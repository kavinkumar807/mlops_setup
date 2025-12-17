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
2) touch eda/data_ingestor.py eda/data_inspection.py
