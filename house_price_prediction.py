import os
import pandas as pd
from eda.data_ingestor import DataIngestorFactory
from eda.data_inspection import DataInspector, DataTypeInspection, SummaryDataInspection
from eda.data_analysis import AnalysisContext, NumericalUnivariateAnalysis, CategoricalUnivariateAnalysis, BivariateHeatmapAnalysis 
from eda.missing_value_handling import MissingValueContext, DropMissingValueStrategy, FillMissingValueStrategy
from eda.data_encoding import DataEncoding

from feature_store.feature_store import FeastFeatureStore
from feature_store.feature_repo.definitions import house, house_features
from feature_store.exec_feature_store import ExecuteFeatureStore 
from datetime import datetime, timedelta

class HousePricePrediction:
    def __init__(self):
        self.df = None

    def load_and_inspect_data(self):
        path =os.path.abspath(os.path.join(os.getcwd(), os.pardir)+ "//mlops_basics/data/Housing.csv")
        file_ext = os.path.splitext(path)[1]
        ingestor_class = DataIngestorFactory.get_data_ingestor(file_ext)
        ingestor = ingestor_class()
        self.df = ingestor.ingest(path)
        print(self.df.head())

        data_inspector = DataInspector(DataTypeInspection())
        data_inspector.inspect_data(self.df)

        data_inspector.set_strategy(SummaryDataInspection())
        data_inspector.inspect_data(self.df)

        # univariate = AnalysisContext(NumericalUnivariateAnalysis())
        # univariate.execute_analysis(self.df, "price")

        # univariate_cat = AnalysisContext(CategoricalUnivariateAnalysis())
        # univariate_cat.execute_analysis(self.df, "guestroom")

    def process_data(self) -> pd.DataFrame:
        #handle_missing_values
        missing_value_handling = MissingValueContext(DropMissingValueStrategy())
        newdf = missing_value_handling.execute_handling(self.df)
        missing_value_handling.set_strategy(FillMissingValueStrategy())
        out_df = missing_value_handling.execute_handling(newdf)
        return self.encode_data(out_df)

    def encode_data(self, df) -> pd.DataFrame:
        binary_columns = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']
        cat_columns = ['furnishingstatus']
        numerical_columns = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking']
        encode = DataEncoding()
        bin_df = encode.binary_encoding(df, binary_columns)
        cat_df = encode.categorical_encoding(bin_df, cat_columns)
        num_df = encode.numerical_scaling(cat_df, numerical_columns)
        return num_df
    
    # <h2> Feast Feature store
    def get_feature_store(self):
        store = ExecuteFeatureStore().get_feature_store()
        return store
    
    def execute_feature_store(self, store=None): 
        if(store is None): 
            store = self.get_feature_store() 
        self.get_historical_features(store) 
        self.get_online_features(store) 

    def get_historical_features(self, store=None, entity_df=None): 
        # if(store is None): 
        #     store = self.get_feature_store() 
        #     store.store.apply([house, house_features]) 

        # if (entity_df is None): 
        #     entity_df = store.get_entity_dataframe(path=os.path.join(os.getcwd() + "//feature_store//data//house_target.parquet")) 

        # features=[ 
        #     "house_features:area", 
        #     "house_features:bedrooms", 
        #     "house_features:mainroad" 
        # ] 
        hist_df = ExecuteFeatureStore().get_historical_features(store, entity_df) 
        return hist_df 
 
    def get_online_features(self, store, entity_df=None): 
        # features=[ 
        #     "house_features:area", 
        #     "house_features:bedrooms", 
        #     "house_features:mainroad" 
        # ] 
        # if (entity_df is None): 
        #     entity_df = store.get_entity_dataframe(path=os.path.join(os.getcwd() + "//feature_store//data//house_target.parquet")) 
        # entity_rows = entity_df.to_dict(orient="records") 

        online_df = ExecuteFeatureStore().get_online_features(store, entity_df)
        return online_df

    def materialize(self, end_date = datetime.now(), start_date=None, increment=False, store=None):
        if(store is None):
            store = self.get_feature_store()
        ExecuteFeatureStore().materialize(end_date, start_date, increment, store)
    


if __name__ == "__main__":
    hpp = HousePricePrediction()
    hpp.load_and_inspect_data()
    processed_df = hpp.process_data()
    print(processed_df.head())
    hpp.execute_feature_store()