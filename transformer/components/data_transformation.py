# Importing Dependencies
import sys

import numpy as np
import pandas as pd
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline

from transformer.constant.training_pipeline import TARGET_COLUMN
from transformer.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact,
)

from transformer.entity.config_entity import DataTransformationConfig
from transformer.exception import SensorException
from transformer.logger import logging
from transformer.ml.model.estimator import TargetValueMapping
from transformer.utils.main_utils import save_numpy_array_data, save_object


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            print(e)


    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            print(e)


    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        """ Creating preprocessing object for data transformation"""
        try:
            robust_scaler = RobustScaler() # initializing RobustScaler
            # Creating preprocessing pipeline
            preprocessor_pipeline = Pipeline(
                steps=[
                    ("RobustScaler", robust_scaler) # Feature scaling and handling outliers
                    ]
            )
            return preprocessor_pipeline

        except Exception as e:
            raise SensorException(e, sys) from e


    def initiate_data_transformation(self,) -> DataTransformationArtifact:
        try:
            print(self.data_validation_artifact.valid_train_file_path)
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path) 
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            print(train_df.shape)
            print(test_df.shape)

            preprocessor_pipeline = self.get_data_transformer_object()


            # Spliting Training DataFrame
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1) # Input Feature
            target_feature_train_df = train_df[TARGET_COLUMN] # Target Feature

            # Spliting Testing DataFrame
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1) # Input Feature
            target_feature_test_df = test_df[TARGET_COLUMN] # Target Feature

            preprocessor_obj = preprocessor_pipeline.fit(input_feature_train_df)

            logging.info(f"Performing PreProcessing(RobustScaler and SimpleImputer) on training data")
            transformed_input_train_feature = preprocessor_obj.transform(input_feature_train_df)

            logging.info(f"Performing PreProcessing(RobustScaler and SimpleImputer) on testing data")
            transformed_input_test_feature =preprocessor_obj.transform(input_feature_test_df)


            smote = SMOTETomek(sampling_strategy="minority")
            
            logging.info(f"Performing SMOTE on training data")
            input_feature_train_final, target_feature_train_final = smote.fit_resample(
                transformed_input_train_feature, target_feature_train_df
            )

            logging.info(f"Performing SMOTE on testing data")
            input_feature_test_final, target_feature_test_final = smote.fit_resample(
                transformed_input_test_feature, target_feature_test_df
            )


            # Concatenating features 
            train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final)]
            test_arr = np.c_[ input_feature_test_final, np.array(target_feature_test_final)]
            

            #  Saving numpy array
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, 
                                  array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path
                                 ,array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path
                        ,preprocessor_obj)
            
            
            # Preparing artifacts
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )

            logging.info(f"Data transformation artifact: {data_transformation_artifact}")

            return data_transformation_artifact

        except Exception as e:
            print(e)
