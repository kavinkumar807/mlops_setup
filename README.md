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
