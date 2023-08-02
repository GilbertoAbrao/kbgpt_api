# GENERAL
prefix      = "kbgpt_api"
environment = "dev"
region      = "us-east-1"
vpc_id      = ""
tags = {
  "Terrform"    = "true"
  "Project"     = "kbgpt_api"
  "Environment" = "hml"
}


# EC2
ec2_instance_type  = "t2.micro"
ec2_instance_port  = 80
ec2_container_port = 8000
ssh_ip_open        = "99.77.72.129"


# ROUTE53
route53_domain_name = "wizeller.com"
route53_subdomain   = "dev-kbgpt-api"
route53_zone_id     = "Z02086393AJ3KVG7B8XQT"


# REPOSITORIO AZURE DEVOPS
git_url    = "https://github.com/GilbertoAbrao/kbgpt_api"
git_branch = "dev"
git_user   = "GilbertoAbrao"
git_token  = "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"
