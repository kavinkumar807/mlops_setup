import os
import pandas as pd
from eda.data_ingestor import DataIngestorFactory
from eda.data_inspection import DataInspector, DataTypeInspection, SummaryDataInspection
from eda.data_analysis import AnalysisContext, NumericalUnivariateAnalysis, CategoricalUnivariateAnalysis, BivariateHeatmapAnalysis 
from eda.missing_value_handling import MissingValueContext, DropMissingValueStrategy, FillMissingValueStrategy
from eda.data_encoding import DataEncoding

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

if __name__ == "__main__":
    hpp = HousePricePrediction()
    hpp.load_and_inspect_data()
    processed_df = hpp.process_data()
    print(processed_df.head())