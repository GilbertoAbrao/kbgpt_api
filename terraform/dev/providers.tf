terraform {

  required_version = ">= 0.13.1"

  required_providers {
    aws   = ">=4.56.0"
    local = ">=2.3.0"
  }

  backend "s3" {
    # config will come from unversioned backend.hcl file!
  }
}

provider "aws" {
  region = var.region
  default_tags {
    tags = var.tags
  }

}
