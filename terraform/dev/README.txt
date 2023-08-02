https://registry.terraform.io/providers/hashicorp/aws/latest/docs

https://github.com/terraform-aws-modules


Commands
terraform init -backend-config=backend.hcl
terraform plan
terraform apply
terraform apply -auto-approve
terraform output [output_name]
terraform workspace new name-of-environment
terraform workspace list
terraform workspace select name-of-environment


Arquivos/pastas que precisam ser deletados de uma posta Terraform copiada de outro projeto para que possa ser executado um novo “terraform init”:

/.terraform
.terraform.lock.hcl
terraform.tfstate
terraform.tfstate.backup
