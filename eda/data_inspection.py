import pandas as pd
from abc import ABC, abstractmethod


# Strategy design pattern

class DataInspection(ABC):
    @abstractmethod
    def inspect(self, df: pd.DataFrame):
        pass

class DataTypeInspection(DataInspection):
    def inspect(self, df: pd.DataFrame):
        print("Data Types and Non null columns")
        print(df.info())

class SummaryDataInspection(DataInspection):
    def inspect(self, df: pd.DataFrame):
        print("Summary for numerical variables")
        print(df.describe().transpose())
        print("\nSummary for categorical variables")
        # print(df.describe(include=['object']))
        print(df.describe(include=['O']))


class DataInspector:
    def __init__(self, strategy: DataInspection):
        self._strategy = strategy

    def set_strategy(self, strategy: DataInspection):
        self._strategy = strategy

    def inspect_data(self, df: pd.DataFrame):
        self._strategy.inspect(df)
