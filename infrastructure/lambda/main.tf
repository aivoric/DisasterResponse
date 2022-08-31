### ------------------
### S3 Objects ###
### ------------------

data "aws_s3_object" "lambda_web" {
  bucket = "ik-udacity"
  key    = "lambda_web.zip"
  # source = "build.zip"
}

data "aws_s3_object" "lambda_ml" {
  bucket = "ik-udacity"
  key    = "lambda_ml.zip"
  # source = "build.zip"
}

data "aws_s3_object" "layer_sklearn_xgboost" {
  bucket = "ik-udacity"
  key    = "lambda_layer_sklearn_xgboost.zip"
  # source = "build.zip"
}

data "aws_s3_object" "layer_pandas_plotly" {
  bucket = "ik-udacity"
  key    = "lambda_layer_pandas_plotly.zip"
  # source = "build.zip"
}

### ------------------
### Lambda Layers ###
### ------------------

# Lambda layer containing sklearn and xgboost libraries
resource "aws_lambda_layer_version" "layer_sklearn_xgboost" {
  s3_bucket     = data.aws_s3_object.layer_sklearn_xgboost.bucket
  s3_key        = data.aws_s3_object.layer_sklearn_xgboost.key
  layer_name = "layer_sklearn_xgboost"
  source_code_hash = "${base64sha256(tostring(data.aws_s3_object.layer_sklearn_xgboost.last_modified))}"
  compatible_runtimes = ["python3.9"]
}

# Lambda layer containing pandas and plotly libraries
resource "aws_lambda_layer_version" "layer_pandas_plotly" {
  s3_bucket     = data.aws_s3_object.layer_pandas_plotly.bucket
  s3_key        = data.aws_s3_object.layer_pandas_plotly.key
  layer_name = "layer_pandas_plotly"
  source_code_hash = "${base64sha256(tostring(data.aws_s3_object.layer_pandas_plotly.last_modified))}"
  compatible_runtimes = ["python3.9"]
}

### ------------------
### Lambda Functions ###
### ------------------

resource "aws_lambda_function" "lambda_web" {
  function_name = "lambda_web"
  s3_bucket     = data.aws_s3_object.lambda_web.bucket
  s3_key        = data.aws_s3_object.lambda_web.key
  role          = aws_iam_role.lambda_role.arn
  handler       = "app.handler"
  source_code_hash = "${base64sha256(tostring(data.aws_s3_object.lambda_web.last_modified))}"
  runtime = "python3.9"
  timeout = 20
  memory_size = 512
  layers = [
    aws_lambda_layer_version.layer_pandas_plotly.arn
  ]
}

resource "aws_lambda_function" "lambda_ml" {
  function_name = "lambda_ml"
  s3_bucket     = data.aws_s3_object.lambda_ml.bucket
  s3_key        = data.aws_s3_object.lambda_ml.key
  role          = aws_iam_role.lambda_role.arn
  handler       = "function.lambda_handler"
  source_code_hash = "${base64sha256(tostring(data.aws_s3_object.lambda_ml.last_modified))}"
  runtime = "python3.9"
  timeout = 20
  memory_size = 512
  layers = [
    // aws_lambda_layer_version.layer_sklearn_xgboost.arn
  ]
}

### ------------------
### Lambda Function URLs ###
### ------------------

resource "aws_lambda_function_url" "lambda_web" {
  function_name      = aws_lambda_function.lambda_web.function_name
  authorization_type = "NONE"
}

### ------------------
### Cloudwatch Log Group ###
### ------------------

resource "aws_cloudwatch_log_group" "cloudwatch_lambda_web" {
  name              = "/aws/lambda/${aws_lambda_function.lambda_web.function_name}"
  retention_in_days = 3
}

resource "aws_cloudwatch_log_group" "cloudwatch_lambda_ml" {
  name              = "/aws/lambda/${aws_lambda_function.lambda_ml.function_name}"
  retention_in_days = 3
}
