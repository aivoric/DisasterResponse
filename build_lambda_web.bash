mkdir -m 777 build_lambda_web
pip install --target build_lambda_web -r requirements-prod.txt
cd build_lambda_web && zip -r9 ../build_lambda_web.zip . && cd ..
cd src/web_app && zip -g ../../build_lambda_web.zip -r . && cd ../..
aws s3 cp ./build_lambda_web.zip s3://ik-udacity/lambda_web.zip
# cd infrastructure && terraform apply -auto-approve && cd ..
rm -rf ./build_lambda_web
rm -r ./build_lambda_web.zip

