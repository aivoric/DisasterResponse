mkdir -m 777 -p build-layer/python/lib/python3.9/site-packages
chmod -R 777 -v build-layer/
pip install \
    --platform manylinux2014_x86_64 \
    --target=build-layer/python/lib/python3.9/site-packages \
    --implementation cp \
    --python 3.9 \
    --only-binary=:all: --upgrade \
    pandas==1.4.3 plotly # scikit-learn xgboost 
# pip install --target build -r requirements-prod.txt
cd build-layer && zip -r9 ../build-layer.zip . && cd ..
# cd src && zip -g ../build.zip -r . && cd ..
aws s3 cp ./build-layer.zip s3://ik-udacity/build-layer.zip
# cd infrastructure && terraform apply -auto-approve && cd ..
rm -r ./build-layer.zip
rm -rf ./build-layer