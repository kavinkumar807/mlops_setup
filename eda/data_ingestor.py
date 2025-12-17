import os
import zipfile
from abc import ABC , abstractmethod
import pandas as pd

# Factory design pattern

# Product
class DataIngestor(ABC):
    @abstractmethod
    def ingest(self, file_path: str) -> pd.DataFrame:
        pass

# Concrete Product - ZipFile Ingestor
class ZipFileIngestor(DataIngestor):
    def ingest(self, file_path: str) -> pd.DataFrame:
        if not file_path.endswith(".zip"):
            raise ValueError("Not a zip file")

        with zipfile.ZipFile(file_path, "r") as file:
            file.extractall("data")

        extracted = os.listdir("data")
        csv_file = [file for file in extracted if file.endswith(".csv")]

        if len(csv_file) == 0:
            raise FileNotFoundError("No CSV file found")
        if len(csv_file) > 1:
            raise ValueError("Multiple CSV files found. Specify one")
                             
        path = os.path.join("data", csv_file[0])
        df = pd.read_csv(path)
        return df
    
# Concrete Product - CSV File Ingestor
class CSVFileIngestor(DataIngestor):
    def ingest(self, file_path: str) -> pd.DataFrame:
        if not file_path.endswith(".csv"):
            raise ValueError("Not a CSV file")
        
        df = pd.read_csv(file_path)
        return df
    
# Concrete Creator
class DataIngestorFactory:
    @staticmethod
    def get_data_ingestor(extension_type: str) -> DataIngestor:
        file_types = {
            ".zip": ZipFileIngestor,
            ".csv": CSVFileIngestor
        }
        ingestor = file_types.get(extension_type, None)
        return ingestor