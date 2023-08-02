
# # Create an S3 bucket
# resource "aws_s3_bucket" "my_bucket" {
#   bucket = "${var.prefix}-tf-${var.environment}-bucket"
# }
# 
# # Create a bucket policy
# resource "aws_s3_bucket_policy" "my_bucket_policy" {
#   bucket = aws_s3_bucket.my_bucket.id
#   policy = data.aws_iam_policy_document.my_bucket_policy_document.json
# }
# 
# # Create a bucket policy document
# data "aws_iam_policy_document" "my_bucket_policy_document" {
#   statement {
#     sid    = "AllowPublicRead"
#     effect = "Allow"
# 
#     principals {
#       type        = "AWS"
#       identifiers = [aws_iam_user.my_user.arn]
#     }
# 
#     actions   = ["s3:*"]
#     resources = ["arn:aws:s3:::${aws_s3_bucket.my_bucket.id}/*"]
#   }
# }
# 
# # Create a bucket CORS configuration
# resource "aws_s3_bucket_cors_configuration" "my_cors_configuration" {
#   bucket = aws_s3_bucket.my_bucket.id
# 
#   cors_rule {
#     allowed_headers = ["*"]
#     allowed_methods = ["PUT", "POST", "DELETE"]
#     allowed_origins = ["*"]
#     expose_headers  = ["ETag"]
#     max_age_seconds = 3000
#   }
# 
#   cors_rule {
#     allowed_methods = ["GET", "HEAD"]
#     allowed_origins = ["*"]
#   }
# }
