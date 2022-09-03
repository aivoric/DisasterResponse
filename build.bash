mkdir -m 777 build
chmod -R 777 -v build
pip install \
    --platform manylinux2014_x86_64 \
    --target=build \
    --implementation cp \
    --python 3.9 \
    --only-binary=:all: --upgrade \
    pandas==1.4.3
pip install --target build -r requirements-prod.txt
cd build && zip -r9 ../build.zip . && cd ..
cd src && zip -g ../build.zip -r . && cd ..
aws s3 cp ./build.zip s3://ik-udacity/v1-lambda-web.zip
cd infrastructure && terraform apply -auto-approve && cd ..
rm -rf ./build
rm -r ./build.zip

