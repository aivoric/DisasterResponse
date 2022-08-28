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
  key    = "build.zip"
  # source = "build.zip"
}

data "aws_s3_object" "ml_lambda_zip" {
  bucket = "ik-udacity"
  key    = "build-layer.zip"
  # source = "build.zip"
}

resource "aws_lambda_layer_version" "ml_lambda_layer" {
  s3_bucket     = data.aws_s3_object.ml_lambda_zip.bucket
  s3_key        = data.aws_s3_object.ml_lambda_zip.key
  layer_name = "ml_lambda_layer"
  source_code_hash = "${base64sha256(tostring(data.aws_s3_object.ml_lambda_zip.last_modified))}"

  compatible_runtimes = ["python3.9"]
}


resource "aws_lambda_function" "ml_lambda" {
  # If the file is not in the current working directory you will need to include a 
  # path.module in the filename.
  # filename      = var.zipfile
  function_name = "ml_lambda"
  s3_bucket     = data.aws_s3_object.s3_lambda_zip.bucket
  s3_key        = data.aws_s3_object.s3_lambda_zip.key
  role          = aws_iam_role.iam_ml_lambda.arn
  handler       = "app.handler"

  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda_function_payload.zip"))}"
  # source_code_hash = data.aws_s3_object.s3_lambda_zip.body
  source_code_hash = "${base64sha256(tostring(data.aws_s3_object.s3_lambda_zip.last_modified))}"
  layers = [aws_lambda_layer_version.ml_lambda_layer.arn]

  runtime = "python3.9"
  timeout = 20
  memory_size = 512

  environment {
    variables = {
      foo = "bar"
    }
  }
}

resource "aws_lambda_function_url" "ml_lambda_url" {
  function_name      = aws_lambda_function.ml_lambda.function_name
  authorization_type = "NONE"
}

