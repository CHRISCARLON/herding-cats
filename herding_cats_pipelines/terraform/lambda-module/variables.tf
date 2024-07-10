variable "aws_region" {
  description = "The AWS region to deploy to"
  type        = string
}

variable "function_name" {
  description = "The name of the Lambda function"
  type        = string
}

variable "code_bucket_name" {
  description = "Name of the existing S3 bucket containing Lambda function code"
  type        = string
}

variable "data_bucket_name" {
  description = "Name of the S3 bucket for Lambda function data operations"
  type        = string
}