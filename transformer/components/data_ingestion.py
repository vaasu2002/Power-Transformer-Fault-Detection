import os
import sys
import pandas as pd

from pandas import DataFrame
from sklearn.model_selection import train_test_split
from transformer.entity.artifact_entity import DataIngestionArtifact
from transformer.entity.config_entity import DataIngestionConfig
from transformer.data_access.transformer_data import TransformerData
from transformer.constant.training_pipeline import SCHEMA_FILE_PATH
from transformer.utils.main_utils import read_yaml_file


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            print(e)


    def export_data_into_feature_store(self,)->pd.DataFrame:
        try:
            transformer_data = TransformerData()
            dataframe = transformer_data.export_collection_as_dataframe()

            # Creating folder
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            dataframe.to_csv(feature_store_file_path, index=False, header=True)

            return dataframe

        except Exception as e:
            print(e)
    

    def split_data_as_train_test(self, dataframe: DataFrame)-> None:
        try:
            train_set,test_set = train_test_split(
                dataframe,test_size = self.data_ingestion_config.train_test_split_ratio
            )

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)

            os.makedirs(dir_path, exist_ok=True)

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )

            
        except Exception as e:
            print(e)


    def initiate_data_ingestion(self,):
        try:
            dataframe = self.export_data_into_feature_store()
            print(dataframe.shape)
            dataframe = dataframe.drop(self._schema_config['drop_columns'],axis=1)
            print(dataframe.shape)
            self.split_data_as_train_test(dataframe)

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path,
            )

            # logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")

            # print(f"Data Ingestion Artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            print(e)