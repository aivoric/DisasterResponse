output "lambda_public_url" {
  value = aws_lambda_function_url.lambda_web.function_url
  description = "The public URL of the lambda."
}