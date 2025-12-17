import os
import pandas as pd
from feast import FeatureStore
from feast.infra.offline_stores.file_source import SavedDatasetFileStorage
from datetime import datetime

class FeastFeatureStore:
    def __init__(self, path: str):
        self.store = FeatureStore(repo_path=path)
        self.retrieval_job = None 

    def get_entity_dataframe(self, path: str) -> pd.DataFrame:
        entity_df = pd.read_parquet(path)
        return entity_df
    
    def get_historical_features(self, entity_df: pd.DataFrame, features: list) -> pd.DataFrame:
        self.retrieval_job = self.store.get_historical_features(
            entity_df=entity_df,
            features=features
        )

        return self.retrieval_job.to_df()
    
    def save_dataset(self, file_name: str, path: str):
        self.store.create_saved_dataset(
            _from=self.retrieval_job,
            name=file_name,
            storage=SavedDatasetFileStorage(path=path)
        )
        print(str.format("File {0} saved successfully", file_name))

    def materialize(self, end_date, start_date=None, incremental: bool=False):
        if not incremental:
            self.store.materialize(
                end_date=end_date,
                start_date=start_date
            )
        else:
            self.store.materialize_incremental(
                end_date=end_date
            )

    def get_online_features(self, features: list, entity_rows: list) -> pd.DataFrame:
        retrieval_job = self.store.get_online_features(
            features=features,
            entity_rows=entity_rows
        )
        return retrieval_job.to_df()