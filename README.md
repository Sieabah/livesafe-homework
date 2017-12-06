# DevOps Homework

# Part 1

The intention behind the assignment is to show understanding of scripting, infrastructure management software, and hopefully the ability to learn new technologies. The following example is in Terraform.

## Premise:

Modern web applications have strict uptime requirements. It is critically important to keep this in mind when designing infrastructure architecture. The assignment here is to produce a terraform configuration file describing a highly redundant VPC. This architecture needs to be resistant to attack, as well as instance and availability zone failure. This VPC must be able to hold a Cassandra cluster, web application behind a load balancer, and a dockerized backend application

Please do not run "terraform apply" as you could incur costs within your aws account.
PLEASE DO NOT UPLOAD YOUR AWS CREDS!!

I particularly liked these links for learning terraform if you are not already familiar:
[terraform.io](https://www.terraform.io/docs/commands/index.html)
[gruntwork blog](https://blog.gruntwork.io/terraform-tips-tricks-loops-if-statements-and-gotchas-f739bbae55f9)

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

#Part 2

## Premise:

Different software works with data is different formats. Here you are given an employee file in a json format, but unfortunately the integration you have been tasked with only works with CSV format. Given the input “employeelist.json” create a script to parse and reformat the file into CSV format.

## Goal

The goal of this assignment is to be able to run a script that reads from employeelist.json and outputs to a csv file

## Submission

* A script to generate csv file
    * This can be in the language of your choosing
* Any other supporting files of the generation
* A README file describing how to execute the script to generate the csv file
    * You may also include any information you want us to see, various attempts that were made, or anything else; that is up to you.
    * A list of any assumptions you made
