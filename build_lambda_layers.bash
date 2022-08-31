# Build sklearn xgboost layer and upload to S3
mkdir -m 777 -p build_layer_sklearn_xgboost/python/lib/python3.9/site-packages
chmod -R 777 -v build_layer_sklearn_xgboost/
pip install \
    --platform manylinux2014_x86_64 \
    --target=build_layer_sklearn_xgboost/python/lib/python3.9/site-packages \
    --implementation cp \
    --python 3.9 \
    --only-binary=:all: --upgrade \
    pandas==1.4.3 scikit-learn xgboost 
cd build_layer_sklearn_xgboost && zip -r9 ../build_layer_sklearn_xgboost.zip . && cd ..
aws s3 cp ./build_layer_sklearn_xgboost.zip s3://ik-udacity/lambda_layer_sklearn_xgboost.zip
rm -r ./build_layer_sklearn_xgboost.zip
rm -rf ./build_layer_sklearn_xgboost


# Build pandas plotly layer and upload to S3
mkdir -m 777 -p build_layer_pandas_plotly/python/lib/python3.9/site-packages
chmod -R 777 -v build_layer_pandas_plotly/
pip install \
    --platform manylinux2014_x86_64 \
    --target=build_layer_pandas_plotly/python/lib/python3.9/site-packages \
    --implementation cp \
    --python 3.9 \
    --only-binary=:all: --upgrade \
    pandas==1.4.3 pandas plotly
cd build_layer_pandas_plotly && zip -r9 ../build_layer_pandas_plotly.zip . && cd ..
aws s3 cp ./build_layer_pandas_plotly.zip s3://ik-udacity/lambda_layer_pandas_plotly.zip
rm -r ./build_layer_pandas_plotly.zip
rm -rf ./build_layer_pandas_plotly