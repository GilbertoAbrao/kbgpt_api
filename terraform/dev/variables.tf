# GENERAL
variable "prefix" {}
variable "environment" {}
variable "region" {}
variable "tags" {}
variable "vpc_id" {}


# EC2
variable "ec2_instance_type" {}
variable "ec2_instance_port" {}
variable "ec2_container_port" {}
variable "ssh_ip_open" {}


# ROUTE53
variable "route53_domain_name" {}
variable "route53_subdomain" {}
variable "route53_zone_id" {}


# REPOSITORIO
variable "git_url" {}
variable "git_branch" {}
variable "git_user" {}
variable "git_token" {}
