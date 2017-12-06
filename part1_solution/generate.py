from typing import Callable, List
from abc import ABC
import ipaddress
import json
import os

class Provider:
    def __init__(self, region='us-east-1'):
       self.__region = region

    def __str__(self):
        return '\n'.join([
            # Hard coded for simplicity
            ' '.join(('provider', '"aws"', '{')),
            '\n'.join([
                'access_key = "'+os.environ.get('AWS_ACCESS_KEY_ID', 'key')+'"',
                'secret_key = "'+os.environ.get('AWS_SECRET_ACCESS_KEY', 'secret')+'"',
                'region = "'+self.__region+'"'
            ]),
            '}\n'
        ])

class Resource:
    def __init__(self, resource_type, name, **kwargs):
        self.__properties = {}
        self.__resource_type = resource_type
        self.__name = name

        for key in kwargs:
            self[key] = kwargs.get(key)

    def __setitem__(self, prop, value):
        self.__properties[prop] = value

    def __getitem__(self, prop):
        return self.__properties.get(prop)

    def __getattr__(self, prop):
        if prop in self.__properties:
            return self.__properties.get(prop)

        return super().__getattribute__(prop)

    def type(self) -> str:
        return self.__resource_type

    def name(self) -> str:
        return self.__name

    def qualifier(self) -> str:
        return '.'.join((self.type(), self.name()))

    def __str__(self) -> str:
        properties = self.__properties

        def stringify_prop(name, props):
            if isinstance(props[name], dict):
                return '\n'.join([
                    ' '.join((name, '{')),
                    '\n'.join([' '.join((subprop, '=', json.dumps(props[name][subprop]))) for subprop in props[name]]),
                    '}'
                ])

            return ' '.join((name, '=', json.dumps(props[name])))

        return '\n'.join([
            ' '.join(('resource', '"'+self.type()+'"', '"'+self.name()+'"', '{')),
            '\n'.join([
                stringify_prop(prop, properties) for prop in properties
            ]),
            '}\n'
        ])

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        for _ in self.__properties.keys():
            yield self.__properties[_]

        raise StopIteration

def ref(res: Resource, value: str or list) -> str:
    """
    Reference resource
    :param res Resource to reference
    :param value Value to reference from resource
    """
    if isinstance(value, (list, tuple)):
        value = '.'.join(value)

    key = '.'.join((res.qualifier(), value))
    return ''.join(('${', key, '}'))

def resource(resource_type: str, name: str, **kwargs) -> Resource:
    """
    Generate resource of type with name
    :param resource_type Resource type
    :param name Name of resource
    :param kwargs Attributes to apply to resource
    """
    return Resource(resource_type, name, **kwargs)

def get_input(display_question: str ='', validate: Callable=lambda a: True):
    """
    Get user input and validate
    :param display_question Prompt to display for input
    :param validate Validation ran on input
    """
    while True:
        _input = input(display_question)

        if validate(_input):
            return _input

def validate(stack) -> List[Resource]:
    """
    Validate resources have unique resource-name pairs
    :param stack Stack to verify
    """
    ids = {}
    for res in stack:
        if isinstance(res, Provider):
            continue

        qualifier = res.qualifier()
        if qualifier in ids:
            raise EnvironmentError(' '.join(('Qualifier', qualifier, 'already exists twice in stack')))

        ids[qualifier] = 1

    return stack

if __name__ == '__main__':
    def validate_cidr_block(value):
        try:
            ipaddress.ip_network(value)
        except ValueError:
            print('Invalid Cidr Block')
            return False

        return True

    stack_name = get_input(display_question='What is the stackname? ')

    # Interface with API to get all current regions, does not validate region
    region = get_input(display_question='Region: ')

    stack = [Provider(region)]

    vpc = resource(
        'aws_vpc', 'main',
        cidr_block = get_input(display_question='What Cidr Block? ', validate=validate_cidr_block),
        enable_dns_support = True,
        enable_dns_hostnames = True,
        tags = { 'Name': stack_name+'VPC' }
    )

    stack.append(vpc)

    # Subnetting, hard coding two, very easily could expand this to do n subnets

    network = ipaddress.ip_network(vpc.cidr_block)
    subnets = list(network.subnets(prefixlen_diff=1))

    subnet1 = resource(
        'aws_subnet', 'primary',
        vpc_id = ref(vpc, 'id'),
        cidr_block = str(subnets[0]),
        map_public_ip_on_launch=True,
        tags = { 'Name': stack_name+'Subnet1' }
    )

    subnet2 = resource(
        'aws_subnet', 'secondary',
        vpc_id = ref(vpc, 'id'),
        cidr_block = str(subnets[1]),
        map_public_ip_on_launch=True,
        tags = { 'Name': stack_name+'Subnet1' }
    )

    stack += [subnet1, subnet2]

    # Routing and Internet

    igw = resource(
        'aws_internet_gateway', 'gw',
        vpc_id = ref(vpc, 'id'),
        tags = { 'Name': stack_name+'igw' }
    )

    stack.append(igw)

    route_table = resource(
        'aws_route_table', 'primary',
        vpc_id = ref(vpc, 'id'),
        # Limitation of only one route with current implementation
        route={
            'cidr_block': '0.0.0.0/0',
            'gateway_id': ref(igw, 'id')
        },
        tags = { 'Name': stack_name+'rt' }
    )

    stack.append(route_table)

    stack += [
        resource('aws_route_table_association', 'subnet1',
            subnet_id=ref(subnet1, 'id'),
            route_table_id=ref(route_table, 'id')),
        resource('aws_route_table_association', 'subnet2',
            subnet_id=ref(subnet2, 'id'),
            route_table_id=ref(route_table, 'id'))
    ]

    # define security groups for applications....

    # add instances...
    # add load balancers
    # etc...

    # Crude unique key validation
    validate(stack)

    with open('stack.tf', 'w') as fp:
        for prop in stack:
            fp.write(str(prop))
