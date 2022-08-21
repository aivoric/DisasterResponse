module "ml_lambda" {
  source      = "./lambda"
  zipfile     = "deploy.zip"
}
