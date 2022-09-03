resource "aws_iam_policy" "lambda_logging" {
  name        = "lambda_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.iam_ml_lambda.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

resource "aws_cloudwatch_log_group" "cloudwatch_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.ml_lambda.function_name}"
  retention_in_days = 3
}

resource "aws_iam_role" "iam_ml_lambda" {
  name = "iam_ml_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

data "aws_s3_object" "s3_lambda_zip" {
  bucket = "ik-udacity"
  key    = "v1-lambda-web.zip"
}

resource "aws_lambda_function" "ml_lambda" {
  function_name = "ml_lambda"
  s3_bucket     = data.aws_s3_object.s3_lambda_zip.bucket
  s3_key        = data.aws_s3_object.s3_lambda_zip.key
  role          = aws_iam_role.iam_ml_lambda.arn
  handler       = "app.handler"

  source_code_hash = "${base64sha256(tostring(data.aws_s3_object.s3_lambda_zip.last_modified))}"

  runtime = "python3.9"
  timeout = 20
  memory_size = 512
}

resource "aws_lambda_function_url" "ml_lambda_url" {
  function_name      = aws_lambda_function.ml_lambda.function_name
  authorization_type = "NONE"
}

