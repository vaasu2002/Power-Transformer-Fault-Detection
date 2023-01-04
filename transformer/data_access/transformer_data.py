import sys
from typing import Optional

import numpy as np
import pandas as pd

from transformer.configuration.mongo_db_connection import MongoDBClient
from transformer.constant.database import DATABASE_NAME,COLLECTION_NAME
from transformer.exception import SensorException


class TransformerData:
    def __init__(self):
        try:
            self.mongo_client = MongoDBClient()

        except Exception as e:
            raise SensorException(e, sys)

    def export_collection_as_dataframe(self,)->pd.DataFrame:
        try:
            db = self.mongo_client.client[self.mongo_client.database_name]
            collection = db[COLLECTION_NAME]
            print(list(collection.find()))
            dataframe = pd.DataFrame(list(collection.find()))
            
            if "_id" in dataframe.columns.to_list():
                dataframe = dataframe.drop(columns=["_id"], axis=1)

            dataframe.replace({"na": np.nan}, inplace=True)


            return dataframe
        except Exception as e:
            raise SensorException(e, sys)


# class SensorData:
#     """
#     This class help to export entire mongo db record as pandas dataframe
#     """

#     def __init__(self):

#         try:
#             self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        

#         except Exception as e:
#             raise SensorException(e, sys)

#     def export_collection_as_dataframe(
#         self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
#         try:

#             if database_name is None:
#                 collection = self.mongo_client.database[collection_name]

#             else:
#                 collection = self.mongo_client[database_name][collection_name]

#             print(list(collection.find()))    

#             df = pd.DataFrame(list(collection.find()))

#             if "_id" in df.columns.to_list():
#                 df = df.drop(columns=["_id"], axis=1)

#             df.replace({"na": np.nan}, inplace=True)

#             return df

#         except Exception as e:
#             raise SensorException(e, sys)