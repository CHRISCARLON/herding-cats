provider "aws" {
  region = var.aws_region
}

# LAMBDA FUNCTION
resource "aws_lambda_function" "herding-cats" {
  function_name = var.function_name
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.lambda_handler"
  memory_size   = 2048
  timeout       = 15
  runtime       = "python3.11"
  s3_bucket     = var.code_bucket_name
  s3_key        = "lambda_herding_cats_jobs.zip"
  source_code_hash = data.aws_s3_object.lambda_code.etag
}

resource "aws_lambda_function_event_invoke_config" "herding-cats_concurrency" {
  function_name                = aws_lambda_function.herding-cats.function_name
  maximum_retry_attempts       = 0
}

# IAM role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "${var.function_name}-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# Lambda basic execution policy
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_role.name
}

# S3 read policy for code bucket
resource "aws_iam_policy" "s3_code_access_policy" {
  name        = "${var.function_name}-s3-code-access-policy"
  path        = "/"
  description = "IAM policy for S3 read access to code bucket from Lambda"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "s3:GetObject",
        "s3:ListBucket"
      ]
      Resource = [
        "arn:aws:s3:::${var.code_bucket_name}",
        "arn:aws:s3:::${var.code_bucket_name}/*"
      ]
    }]
  })
}

# S3 read/write policy for the data bucket
resource "aws_iam_policy" "s3_data_access_policy" {
  name        = "${var.function_name}-s3-data-access-policy"
  path        = "/"
  description = "IAM policy for S3 read and write access to the data bucket from Lambda"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ]
      Resource = [
        "arn:aws:s3:::${var.data_bucket_name}",
        "arn:aws:s3:::${var.data_bucket_name}/*"
      ]
    }]
  })
}

# Attach S3 code access policy to Lambda role
resource "aws_iam_role_policy_attachment" "lambda_s3_code_access" {
  policy_arn = aws_iam_policy.s3_code_access_policy.arn
  role       = aws_iam_role.lambda_role.name
}

# Attach S3 data access policy to Lambda role
resource "aws_iam_role_policy_attachment" "lambda_s3_data_access" {
  policy_arn = aws_iam_policy.s3_data_access_policy.arn
  role       = aws_iam_role.lambda_role.name
}


data "aws_s3_object" "lambda_code" {
  bucket = var.code_bucket_name
  key    = "lambda_herding_cats_jobs.zip"
}