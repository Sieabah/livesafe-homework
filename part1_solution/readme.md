## Usage

    python generate.py

It will prompt you for various components.

## Details

What this generates is a singular VPC with two subnets, both subnets automatically map a public IP for instances to actually have access to the IGW. Alternatively this can be done with public/private subnets where your public subnets each have a IGW and your private subnets have a NAT Gateway. What would be idea is splitting the subnets in half so 2 are in each availability zone so the IGW is in close proximity to the nat gateway in the AZ.

There are numerous improvements that can be made to this generator. Mainly, a better way to use it and clean it up. For a rough HW assignment it's probably fine.

## Notes

Funny enough I *just* did something like this for generating cloudformation scripts using [Troposphere](https://github.com/cloudtools/troposphere).

Due to the nature of how oddly specific this solution is I don't feel it's necessary to provide a full fledged vpc creation tool. It also seems odd to script a scriptable state.

I also couldn't really find any library to interface with creating configs so I threw together something rough to generate it similar to troposphere.

# Prompt

## Premise:

Modern web applications have strict uptime requirements. It is critically important to keep this in mind when designing infrastructure architecture. The assignment here is to produce a terraform configuration file describing a highly redundant VPC. This architecture needs to be resistant to attack, as well as instance and availability zone failure. This VPC must be able to hold a Cassandra cluster, web application behind a load balancer, and a dockerized backend application

## Goal

The goal of the exercise is to run ”terraform plan” against the .tf file and see a valid execution plan.

## Submission

Please submit your assignment inside the submission directory.

You should submit the following:

* A script to generate .tf file
    * This can be in the language of your choosing
* Example .tf file from execution
* Any other supporting files of the generation
* A README file describing how to execute the script to generate the .tf file
    * You may also include any information you want us to see, various attempts that were made, or anything else; that is up to you.
    * A list of any assumptions you made
