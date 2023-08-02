resource "aws_key_pair" "my-key-pair" {
  key_name   = "${var.prefix}-${var.environment}-tf-key-pair"
  public_key = tls_private_key.rsa.public_key_openssh
}

resource "tls_private_key" "rsa" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "local_file" "tf-key" {
  content  = tls_private_key.rsa.private_key_pem
  filename = "${aws_key_pair.my-key-pair.key_name}.pem"
}

# OUTPUTS
output "change_key_file_permissions" {
  value = "chmod 400 ${aws_key_pair.my-key-pair.key_name}.pem"
}
