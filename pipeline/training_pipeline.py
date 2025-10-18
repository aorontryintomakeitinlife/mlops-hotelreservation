##without making this trainingpiplinepy into a package we cannot import classes dfrom modeltrainignpy, daaingestionpy datapreprocessingpy etc..
import os
from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTraining
from config.paths_config import *
from utils.common_functions import read_yaml


if __name__=="__main__":
    ###first data ingestion
    data_ingestion=DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()

    ##data processing
    processor=DataProcessor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESSED_DIR,CONFIG_PATH)
    processor.process()

    ##model training
    trainer=ModelTraining(PROCESSED_TRAIN_DATA_PATH,PROCESSED_TEST_DATA_PATH,MODEL_OUTPUT_PATH)
    trainer.run()

##after this we move to data versioning anf code ersioning