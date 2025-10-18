##all code for model training and exp tracking
import os
import pandas as pd

import joblib       ##used for model saving
import lightgbm as lgb
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_functions import read_yaml,load_data
from scipy.stats import randint
import mlflow 
import mlflow.sklearn


logger=get_logger(__name__)
class ModelTraining:

    def __init__(self,train_path,test_path,model_output_path):
        self.train_path=train_path
        self.test_path=test_path
        self.model_output_path=model_output_path##model saved here in this path
        ###initialize rsndom search param and light gbm params
        self.random_search_params=RANDOM_SEARCH_PARAMS
        self.params_dist=LIGHTGM_PARAMS


    def load_and_split_data(self):
        try:
            logger.info(f"loading datafrom {self.train_path}")
            train_df= load_data(self.train_path)
            logger.info(f"loading datafrom {self.test_path}")
            test_df= load_data(self.test_path)
             ###in train_df ,processedtain.csv(in atifact folder) is stored and same for test also 
            ##order and featires shoud be same in prcessed train and processedtest
            X_train=train_df.drop(columns=["booking_status"])
            y_train=train_df["booking_status"]
            X_test=test_df.drop(columns=["booking_status"])
            y_test=test_df["booking_status"]
            logger.info("data splitted sucessfully for model training")
            return X_train,X_test,y_train,y_test
        except Exception as e:
            logger.error(f"error while loading {e}")
            raise CustomException("failed to load data", e)
    ##now training model   
    def train_lgbm(self,X_train,y_train):
        try:
            logger.info("initilaing our model")
            lgbm_model=lgb.LGBMClassifier(random_state=self.random_search_params["random_state"])
            logger.info("starting our hyperparameter tuning")
            random_search=RandomizedSearchCV(estimator=lgbm_model,param_distributions=self.params_dist,
                                             n_iter=self.random_search_params["n_iter"],
                                             cv=self.random_search_params["cv"],
                                             random_state=self.random_search_params["random_state"],
                                             scoring=self.random_search_params["scoring"],
                                             n_jobs=self.random_search_params["n_jobs"],
                                             verbose=self.random_search_params["verbose"]
            )
            logger.info("starting out hyperparameter tuning training")
            random_search.fit(X_train,y_train)
            logger.info("hyperparameter tuning completed")
            ###now we need best parameters , we ll store it allin a variabke bestparmas
            best_params=random_search.best_params_
            best_lgbm_model=random_search.best_estimator_ ##best model ste=ored in ths variable
            logger.info(f"best paramrters are :{best_params}")
            return best_lgbm_model
        except Exception as e:
            logger.error(f"error while training mode; {e}")
            raise CustomException("failed to train model", e)
    def evaluate_model(self,model,X_test,y_test):

        try:
            logger.info("evaluating our model")
            y_pred=model.predict(X_test)
            ##above we are doing model.predict andnot bestlgbmmodel.predict, casue we are passing model in the function definition
            accuracy=accuracy_score(y_test,y_pred)
            precision=precision_score(y_test,y_pred)
            recall=recall_score(y_test,y_pred)
            f1=f1_score(y_test,y_pred)
            logger.info(f"accuracy score:{accuracy}")
            logger.info(f"precision score:{precision}")
            logger.info(f"recall score:{recall}")
            logger.info(f"f1 score:{f1}")
            
            ##we are returning these metrics in a dict formrt and we retun because
            ##
            return {"accuracy":accuracy,"precision":precision,"recall":recall,"f1":f1}
        except Exception as e:
            logger.error(f"error while evaluating model:{e}")
            raise CustomException("failed to evaluate model", e)
        
    ###now to save the model
    def save_model(self,model):
        try:
            ##first vheck if output ditectory exist
            os.makedirs(os.path.dirname(self.model_output_path),exist_ok=True)
            logger.info(f"saving model to {self.model_output_path}")
            joblib.dump(model,self.model_output_path)
            logger.info(f"model saved sucessfully to {self.model_output_path}")
        except Exception as e:
            logger.error(f"error while saving model {e}")
            raise CustomException("failed to save model", e)
    def run(self):
        try:
            with mlflow.start_run(): ###this means when run method is called mlflow will also start
                
                logger.info("starting our model training pipeline")
                
                logger.info("starting our mlflow experimnetation") ##now we need to log our dataset which was used to train this moddel
                logger.info("loggong the traing and testing dataset to mlflow")
                mlflow.log_artifact(self.train_path, artifact_path="datasets") ##our train dataset is in self.ytsrainpath in mlflow a "datasets" folder os created and train is stored in it 
                mlflow.log_artifact(self.test_path , artifact_path="datasets")

                X_train,X_test,y_train,y_test=self.load_and_split_data() ##has no argument only self
                best_lgbm_model=self.train_lgbm(X_train,y_train)
                metrics=self.evaluate_model(best_lgbm_model,X_test,y_test)
                self.save_model(best_lgbm_model)
                logger.info("logging the model into mlflow")
                mlflow.log_artifact(self.model_output_path)
                logger.info("logging params and metrics to mlflow")
                mlflow.log_params(best_lgbm_model.get_params())
                mlflow.log_metrics(metrics) ###for this we returned metrics in a dict , and is stored in a variable "metrics"

                logger.info("model training sucessfully completed")
        except Exception as e:
            logger.error(f"error in model training pipeline {e}")
            raise CustomException("failed to model trainign pipeline", e)

if __name__=="__main__":
        trainer=ModelTraining(PROCESSED_TRAIN_DATA_PATH,PROCESSED_TEST_DATA_PATH,MODEL_OUTPUT_PATH)
        trainer.run()

            
            
###we use mlflow here to keep track of our model,llile our trainig model will have different accuracies as we improve it in step by steps , these different versions of model are saved using sa mlflow
            

            

            
            

            
        



        



