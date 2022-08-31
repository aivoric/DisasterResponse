mkdir -m 777 build_lambda_ml
cd src/ml_lambda && zip -g ../../build_lambda_ml.zip -r . && cd ../..
aws s3 cp ./build_lambda_ml.zip s3://ik-udacity/lambda_ml.zip
rm -rf ./build_lambda_ml
rm -r ./build_lambda_ml.zip

