locals {
  clone_url = replace(var.git_url, "github.com", "${var.git_user}:${var.git_token}@github.com")
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-20230325"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}


resource "aws_instance" "my_ec2" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.ec2_instance_type
  key_name               = aws_key_pair.my-key-pair.key_name
  vpc_security_group_ids = [aws_security_group.my_ec2_sg.id]

  tags = {
    "Name" = "${var.prefix}-${var.environment}-tf"
  }

  user_data = <<-EOF
    #!/usr/bin/bash
    echo "Terraform: Iniciando a instalacao do Docker e do Nginx via user_data do EC2"
    sudo apt update -y
    sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository -y "deb [arch=amd64] https://download.docker.com/linux/ubuntu  $(lsb_release -cs)  stable"
    sudo apt update -y
    sudo apt-get install -y docker-ce
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker ubuntu
    sudo apt-get install -y nginx

    echo -e 'server {
        server_name ${var.route53_subdomain}.${var.route53_domain_name};
        access_log /var/log/nginx/reverse-access.log;
        error_log /var/log/nginx/reverse-error.log;
        location / {proxy_pass http://127.0.0.1:${var.ec2_container_port};}     
    }' | sudo tee /etc/nginx/sites-available/${var.route53_subdomain}.${var.route53_domain_name} > /dev/null

    sudo ln -s /etc/nginx/sites-available/${var.route53_subdomain}.${var.route53_domain_name} /etc/nginx/sites-enabled/${var.route53_subdomain}.${var.route53_domain_name}
    sudo service nginx restart
    sudo apt-get install docker-compose -y

    echo "Terraform: Istalando Certbot"
    
    sudo apt-get install certbot -y
    sudo apt-get install python3-certbot-nginx
    sudo certbot --nginx --non-interactive --agree-tos --register-unsafely-without-email -d ${var.route53_subdomain}.${var.route53_domain_name} -d ${var.route53_subdomain}.${var.route53_domain_name}

    echo "Terraform: Clona o repositorio do projeto e executa o container"

    sudo mkdir /home/${var.prefix}
    sudo git clone -b ${var.git_branch} ${local.clone_url} /home/${var.prefix}
    cd /home/${var.prefix}/
    docker build -t ${var.prefix}-image .
    docker run -d -p ${var.ec2_instance_port}:${var.ec2_container_port} --env-file .env-${var.environment} --name ${var.prefix}-container ${var.prefix}-image

    echo "Terraform: Script concluido"
  EOF
}


resource "aws_eip" "my-eip" {
  vpc = true
}

resource "aws_eip_association" "my-eip_assoc" {
  instance_id   = aws_instance.my_ec2.id
  allocation_id = aws_eip.my-eip.id
}



# create a ec2 security group
resource "aws_security_group" "my_ec2_sg" {
  name_prefix = "${var.prefix}-${var.environment}-tf-sg-"
  description = "Security group for EC2"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # allow ssh access from specific ip address
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${var.ssh_ip_open}/32"]
  }

  # egress rule to allow all outbound traffic

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}




# OUTPUTS
output "server_private_ip" {
  value = aws_instance.my_ec2.private_ip
}

output "server_id" {
  value = aws_instance.my_ec2.id
}

output "elastic_ip" {
  value = aws_eip.my-eip.public_ip
}

output "url_app" {
  value = "https://${var.route53_subdomain}.${var.route53_domain_name}"
}


output "ssh_conection_command" {
  value = "ssh -i ${aws_key_pair.my-key-pair.key_name}.pem ubuntu@${aws_eip.my-eip.public_ip}"

  depends_on = [
    aws_instance.my_ec2,
    aws_key_pair.my-key-pair,
    aws_eip.my-eip,
    aws_eip_association.my-eip_assoc
  ]

}
