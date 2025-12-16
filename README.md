# house_price_mlops

pip install -r requirements.txt
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