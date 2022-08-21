rm -r infrastructure/deploy.zip
mkdir deploy
pip install --target deploy -r prod-requirements.txt
cd deploy && zip -r9 ../infrastructure/deploy.zip .
cd ../src && zip -g ../infrastructure/deploy.zip -r .
cd .. && rm -rf deploy
cd infrastructure && terraform apply -auto-approve
rm -r infrastructure/deploy.zip