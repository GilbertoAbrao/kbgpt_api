
# create subdomain heading to the elastic IP
resource "aws_route53_record" "this" {
  zone_id = var.route53_zone_id
  name    = "${var.route53_subdomain}.${var.route53_domain_name}"
  type    = "A"
  ttl     = 300
  records = [aws_eip.my-eip.public_ip]
}
