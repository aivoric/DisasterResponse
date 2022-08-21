output "lambda_public_url" {
  value = aws_lambda_function_url.ml_lambda_url.function_url
  description = "The public URL of the lambda."
}
# test