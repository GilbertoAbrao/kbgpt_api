# select default VPC
data "aws_vpc" "my_default_vpc" {
  default = true
}


# get all subnets in a VPC
data "aws_subnets" "my_subnet_list" {
  filter {
    name   = "vpc-id"
    values = [var.vpc_id != "" ? var.vpc_id : data.aws_vpc.my_default_vpc.id]
  }
}

# get all network interfaces in a VPC
data "aws_network_interfaces" "example" {
  filter {
    name   = "vpc-id"
    values = [var.vpc_id != "" ? var.vpc_id : data.aws_vpc.my_default_vpc.id]
  }
}
