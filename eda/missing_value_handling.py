import pandas as pd
from abc import ABC, abstractmethod

class MissingValueHandlingStrategy(ABC):
    @abstractmethod
    def handle(self, df: pd.DataFrame) -> pd.DataFrame:
        pass


class DropMissingValueStrategy(MissingValueHandlingStrategy):
    def handle(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.dropna()
    
class FillMissingValueStrategy(MissingValueHandlingStrategy):
    def handle(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.fillna(0)
    
class MissingValueContext:
    def __init__(self, strategy: MissingValueHandlingStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: MissingValueHandlingStrategy):
        self._strategy = strategy

    def check_missing(self, df: pd.DataFrame) -> pd.Series: 
        return df.isnull().sum().sort_values(ascending=False)

    def execute_handling(self, df: pd.DataFrame) -> pd.DataFrame:
        return self._strategy.handle(df)