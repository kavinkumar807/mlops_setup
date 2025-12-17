from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pd

class DataEncoding:
    def __init__(self):
        self.scaler = StandardScaler()

    def binary_encoding(self, data: pd.DataFrame, binary_columns) -> pd.DataFrame:
        # Encoding categorical variables with two categories
        for column in binary_columns:
            data[column] = data[column].apply(lambda x: 1 if x == 'yes' else 0)
            # data[column] = data[column].map({'yes': 1, 'no': 0})
        return data
        
    def categorical_encoding(self, data: pd.DataFrame, cat_columns) -> pd.DataFrame:
        # Encoding categorical variables with more than two categories
        label_encoder = LabelEncoder()
        for column in cat_columns:
            data[column] = label_encoder.fit_transform(data[column])
        return data
    
    def numerical_scaling(self, data: pd.DataFrame, num_columns) -> pd.DataFrame:
        # Scaling numerical variables
        data[num_columns] = self.scaler.fit_transform(data[num_columns])
        return data