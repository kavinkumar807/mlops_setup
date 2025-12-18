# house_price_mlops

# project setup

## clone and install dependencies
git clone https://dagshub.com/kavinkumarbaskar/house_price_mlops.git .   

python3 -m venv .venv  
source ./.venv/bin/activate   
pip install -r requirements.txt

## dvc new initial setup
dvc init
dvc remote add origin https://dagshub.com/kavinkumarbaskar/house_price_mlops.dvc
dvc remote default origin
dvc add data
dvc remote modify origin --local auth basic
dvc remote modify origin --local user "kavinkumarbaskar"
dvc remote modify origin --local password "YOUR_TOKEN"
git add 
git commit -m "data-versioning-setup-completed"
git push -u origin main

## dvc setup
dvc remote add origin https://dagshub.com/kavinkumarbaskar/house_price_mlops.dvc
dvc remote default origin
dvc remote modify origin --local auth basic
dvc remote modify origin --local user "kavinkumarbaskar"
dvc remote modify origin --local password "YOUR_TOKEN"
dvc pull

# add this 
MLFLOW_TRACKING_USERNAME=kavinkumarbaskar
MLFLOW_TRACKING_PASSWORD=<Password/token>
MLFLOW_TRACKING_URI=https://dagshub.com/kavinkumarbaskar/dagshub_basics.mlflow

# new branch
git checkout -b "branch-name"
dvc checkout



# learning

## Data processing

1) mkdir eda
2) touch eda/data_ingestor.py eda/data_inspection.py eda/data_analysis.py eda/missing_value_handling.py eda/data_encoding.py
3) add playground
4) save processed data


## Feature store
1) feast init feature_store -t postgres
2) add data
3) add playground
4) run postgres in docker
5) created db
6) add everthing in .env and update the feast.yaml
7) split data and add to postgres
8) create parquet files and add to dvc
9) add definitions
10) move to root and execute export $(cat .env | xargs) and verify echo $POSTGRE_SQL_PORT
11) cd feature_repo and feast apply
12) feast entities list
13) feast feature-views list
14) feast ui
15) testing file to set example
16) pytest ./testing/testcases.py

## Experiment tracking (MLFLOW)
1) Install mlflow, psycopg2
2) mlflow server --backend-store-uri postgresql+psycopg://postgres:****@localhost:5432/mlflow_tracking_database  --host 127.0.0.1 --port 5000
3) try with local mlflow and switch to dagshub mlflow
```
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("local_experiments")

with mlflow.start_run():
    mlflow.log_metric("rmse", 0.42)

mlflow.set_tracking_uri("https://dagshub.com/<user>/<repo>.mlflow")
mlflow.set_experiment("dagshub_experiments")

with mlflow.start_run():
    mlflow.log_metric("rmse", 0.42)

```

## Model Serving
1) install bentoml and torch transformers # additional dependencies for local run
2) export BENTOML_HOME=./bentoml_store
3) create the service file and playground
4) bentoml models list
5) go to serving folder bentoml serve service:HouseService
6) bentoml build -f serving/bentofile.yaml
    * Deploy to BentoCloud:
        $ bentoml deploy house_service:fja2avg3okuqwbwn -n ${DEPLOYMENT_NAME}

    * Update an existing deployment on BentoCloud:
        $ bentoml deployment update --bento house_service:fja2avg3okuqwbwn ${DEPLOYMENT_NAME}

    * Containerize your Bento with `bentoml containerize`:
        $ bentoml containerize house_service:fja2avg3okuqwbwn 

    * Push to BentoCloud with `bentoml push`:
        $ bentoml push house_service:fja2avg3okuqwbwn 
7) bentoml list
8) bentoml containerize house_service:fja2avg3okuqwbwn 
9) docker run --rm -p 3000:3000 house_service:fja2avg3okuqwbwn

## Model Monitoring
1) Add monitoring files
2) evidently ui --workspace "House Price Monitoring Workspace"

## CI/CD
git remote add origin-git https://github.com/kavinkumar807/mlops_setup.git
git remote set-url origin-git https://USERNAME:TOKEN@github.com/kavinkumar807/mlops_setup.git
git remote -v   
git push -u origin-git main
add deepchecks
Deepchecks is an open-source Python tool used in machine learning to validate and test datasets, models, and entire ML workflows so you can trust them before and after deployment.
Deepchecks runs checks on your datasets to find issues such as:
missing values, inconsistent schemas, duplicates and anomalies
distribution mismatches between train/test or reference vs production data
This helps catch data quality issues before they affect training or predictions
Teach about github actions and self hosted runners

