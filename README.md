# Disaster Response Pipeline Project

### Introduction

The goal of this project was to learn:
1) How to clean text data by building an ETL pipeline
2) How to build a machine learning pipeline for training a multi-class text classification model
3) How to build a web app using FastAPI and deploy it to AWS Lambda

This was possible thanks to a dataset provided by Udacity in the Data Scientist Nanodegree along with guidance
on how to build ETL and ML pipelines. Thank you Udacity!

### Quick start

Clone the repo:
```
git clone https://github.com/aivoric/DisasterResponse.git
cd disasterresponse
```

Install pyenv with virtual env (mac instructions):
```
brew update
brew install pyenv
brew install pyenv-virtualenv (for also managing python environments)
pyenv install -v 3.9
pyenv virtualenv 3.9 disaster-response
pyenv activate disaster-response
```

Install dev requirements:
```
pip install -r requirements-dev.txt
```

To run the ETL pipeline:
```
cd ml
python process_data.py
```

To run the ML pipeline (train the model):
```
python train_classifier.py
```

To launch the web app (FastAPI python app via uvicorn)
```
cd .. (return to root of project)
uvicorn web:app --reload
```

### File overview

* `ml` folder contains the scripts for the ETL and ML pipelines
* `src/app` folder contains the entire web app built via FastAPI
* `src/infrastructure` folder contains Terraform scripts for creating AWS infrastruture in order to deploy the app
* `build.bash` file packages for app for Lambda deployment
* `requirements-dev.txt` contains all the development dependencies
* `requirements-prod.txt` contains all the production dependencies (excluding pandas which is installed separately)

### Results

Below are the results after training the model. The "pretty" table results in the terminal are achieved
by the python tabulate package: https://pypi.org/project/tabulate/

![Disaster Response Results](https://github.com/aivoric/DisasterResponse/blob/main/results/model-results.png?raw=true)

Web app home:
![Disaster Response Results](https://github.com/aivoric/DisasterResponse/blob/main/results/webapp-home.png?raw=true)

Web app classification results after running the query "This group of people needs water, food and money since they are refugees who escaped military oppression.":
![Disaster Response Results](https://github.com/aivoric/DisasterResponse/blob/main/results/webapp-ml.png?raw=true)


### Deploying the app to AWS Lambda

To deploy the model to production (AWS Lambda):

1. Copy the Disaster Response database and the trained pickled pipeline from ml/data and ml/models to the web app src/app/database and src/app/ml/pipeline.pkl
2. Install terraform and aws cli
3. Setup the AWS cli with your production account: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
4. Run `bash build.bash` which will package all the files and deployment via terraform

IMPORTANT:
* The incomplete web app is available here: https://o22bvwrb33ce4gwi4fnckemtmm0ozrus.lambda-url.eu-central-1.on.aws/
* Production deployment is not currently complete
* During an attempt to deploy this app to AWS Lambda I've discovered that Pandas, SKLearn, XGBoost, and Plotly are very heavy dependencies and lambda has a limit for the overall zipped
deployment package file size: https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html
   * 50 MB (zipped, for direct upload)
   * 250 MB (unzipped)
* The web app will only load the front page and display the Database results, however the prediction will not work because SKLearn and XGBoost are not currently packaged during the build
* To address this problem I need to package the entire app in a container and then deploy that via Lambda because Lambdas allow for a 10GB image to be deployed via containers.
* When creating a zipped package for lambda some modules are installed using your local machine architecture and hence will not work on Linux based Lambdas. One particular library affected by this is Pandas. To get around this you need to install the library using a target platform architecture. Below is how this can be done for pandas:

```
pip install \
    --platform manylinux2014_x86_64 \
    --target=build \
    --implementation cp \
    --python 3.9 \
    --only-binary=:all: --upgrade \
    pandas==1.4.3
```

### Future improvements
* Add a custom scoring function to the ML pipeline
* Finish Lambda deployment most likely via containers due to size resrictions
* Add tests.
* Improve the UI of the web app.
* Improve code quality. Certain classes contain tech debt.
* Improve CICD: 1) start using github action, 2) save the terraform state either in the terraform cloud or on S3