from transformer.configuration.mongo_db_connection import MongoDBClient
from transformer.exception import SensorException
from transformer.logger import logging
from transformer.pipeline.training_pipeline import TrainPipeline
if __name__ == '__main__':
    train_pipeline = TrainPipeline()
    train_pipeline.run_pipeline()