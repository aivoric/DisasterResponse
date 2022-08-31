### ---------------------------------------------
### IAM Role: Lambda execution role
### ---------------------------------------------

resource "aws_iam_role" "lambda_role" {
  name = "lambda_role"
  assume_role_policy = data.aws_iam_policy_document.lambda_role_assume_policy.json
}

data "aws_iam_policy_document" "lambda_role_assume_policy" {
  statement {
    actions = ["sts:AssumeRole"]
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    
  }
}

### ---------------------------------------------
### IAM Policy Attachment: Attach policies to role
### ---------------------------------------------

resource "aws_iam_role_policy_attachment" "lambda_role_policy_1" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

resource "aws_iam_role_policy_attachment" "lambda_role_policy_2" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.ml_lambda_invocation.arn
}



### ---------------------------------------------
### IAM Policy: Allow to create logs
### ---------------------------------------------

resource "aws_iam_policy" "lambda_logging" {
  name        = "lambda_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"
  policy      = data.aws_iam_policy_document.logs_access.json
}

data "aws_iam_policy_document" "logs_access" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = [
      "arn:aws:logs:*:*:*",
    ]
  }
}

### ---------------------------------------------
### IAM Policy: Allow to invoke a different Lambda
### ---------------------------------------------

resource "aws_iam_policy" "ml_lambda_invocation" {
  name        = "ml_lambda_invocation"
  path        = "/"
  description = "IAM policy for invoking the ML lambda."
  policy      = data.aws_iam_policy_document.lamda_invocation.json
}

data "aws_iam_policy_document" "lamda_invocation" {
  statement {
    actions = [
      "lambda:InvokeFunction",
      "lambda:InvokeAsync"
    ]
    resources = [
      "arn:aws:lambda:eu-central-1:${aws_lambda_function.lambda_ml.arn}:function:${aws_lambda_function.lambda_ml.function_name}",
    ]
  }
}
