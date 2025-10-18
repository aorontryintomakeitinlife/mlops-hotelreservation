import os
import pandas as pd
import numpy as np ##log trans done w numpy

from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml,load_data
##we did feature selection thoruh randomforestcf in jupyter testing so
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
## we did smote using imbalaced learn so we pip install in terminal
from imblearn.over_sampling import SMOTE

logger=get_logger(__name__) ###name -magic method

class DataProcessor:###parameters of the constyructor are in brakets
    def __init__(self,train_path,test_path,processed_dir,config_path):   ### we pass train parth as object of this class, this train path is from wheere we take data. we do data prcess steps on both train and test data, prcesseddir is where we store the data
        self.train_path=train_path
        self.test_path=test_path
        self.processed_dir=processed_dir
        self.config= read_yaml(config_path)

        ### till now we ahve no processed disrectory in artifact folder so we needto crrate thst
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir) ## we can also do exist ok =true method
    def preprocess_data(self,df):
        try:
            logger.info("starting data processing")
            logger.info("droppinf the colunmns")
            df.drop(columns=['Booking_ID'],inplace=True)
            df.drop_duplicates(inplace=True)

            ###define all cat col and num col extract from yml file
            cat_cols=self.config["data_processing"]["categorical_columns"]
            num_cols=self.config["data_processing"]["numerical_columns"]

            ###the data analysis part in notebokk not important as it was done for insights  

            logger.info("applying label encoding")
            label_encoder=LabelEncoder()
            mappings={}
            for col in cat_cols:
                df[col]=label_encoder.fit_transform(df[col])
                mappings[col]= {label: code for label, code in zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_))}
            logger.info("label mappings are")
            for col,mapping in mappings.items():
                logger.info(f"{col}:{mapping}")
            #### after label encoding we checkied for multicollinearity but our data did not have any so skip
            ##also corrrealtion srep aslo was like visualization no change in data
            ## then we did skewness and we made change to dta
            logger.info("doing skewness handling")
            skew_threshold=self.config["data_processing"]["skewness_threshold"]
            ## WE APPLY SKEWNESS TO ONLY NUMERICALCOLUMNS
            skewness=df[num_cols].apply(lambda x: x.skew())
            for column in skewness[skewness>skew_threshold].index: ###whever grester we get out skewness df inside this m, stored iin skewness variable
                df[column]=np.log1p(df[column])
            return df
        except Exception as e:
            logger.error(f"error during preprocess step {e}")
            raise CustomException("failed to preprocess data",e)
        ####3so far data cleaning is completed in put way
    def balance_data(self,df):## taking the df from preprocess step

        try:
            logger.info("handling imbalanced data")
            X=df.drop(columns=["booking_status"])
            y=df["booking_status"]
            smote=SMOTE(random_state=42)
            X_resampled,y_resampled=smote.fit_resample(X,y) ##this is basical y x resampled amd y resampled
            balanced_df=pd.DataFrame(X_resampled,columns=X.columns)
            balanced_df["booking_status"]=y_resampled
            logger.info("data balanced sucessfyly")
            return balanced_df
        except Exception as e:
            logger.error(f"error while balancinf data {e}")
            raise CustomException("failed to balance data",e)
    

    ###doinf feture selection
    def select_features(self,df):
        try:
            logger.info("starting feature selection step")
            X=df.drop(columns=["booking_status"])
            y=df["booking_status"]
            ##initializing out model
            model=RandomForestClassifier(random_state=42)
            model.fit(X,y)
            feature_importance=model.feature_importances_
            feature_importance_df=pd.DataFrame({"feature":X.columns,"importance":feature_importance})
            top_features_importance_df=feature_importance_df.sort_values(by="importance",ascending=False)
            num_features_to_select=self.config["data_processing"]["no_of_features"]
            top_10_features=top_features_importance_df["feature"].head(num_features_to_select).values
            logger.info(f"features selected:{top_10_features}")
            top_10_df=df[top_10_features.tolist() + ["booking_status"]]
            logger.info("feature selection completed")
            return top_10_df
        except Exception as e:
            logger.error(f"error during feature selection {e}")
            raise CustomException("error to to select features",e)
        ###finally model selection above this till here data prcessing complete data 10 is clean dta, we got clean dataframe now we going to save the data frame into csv file##
    def save_data(self,df,file_path):
        try:
            logger.info(f"saving data to prcessed foledr")
            df.to_csv(file_path,index=False) ## false casue unnecassry column gets created
            logger.info(f"data saved sucesfully to {file_path}")
        except Exception as e:
            logger.error(f"error while saving data {e}")
            raise CustomException("failed to save data",e )
    def process(self):## same like what did in data inestion all steps will be combined
        try:
            logger.info("loading data from raw directory")
            train_df=load_data(self.train_path)###the train path deffined in def data processing in the top of this file
            test_df=load_data(self.test_path) ###these are our dataframes

            train_df=self.preprocess_data(train_df)
            test_df=self.preprocess_data(test_df)
            train_df=self.balance_data(train_df)
            test_df=self.balance_data(test_df)###actually noneed to balance test df

            train_df=self.select_features(train_df)
            test_df=test_df[train_df.columns]
            ##top 10 featres can be diff for train and test df ,
            ###but with the above code testdf=testdf , both will use the same features
            self.save_data(train_df,PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df,PROCESSED_TEST_DATA_PATH)
            logger.info("data processing completed")
        except Exception as e:
            logger.error(f"error during data preprocessing pipeline {e}")
            raise CustomException("error whiel data preprcessing pipeline",e)
if __name__=="__main__": ## whatever we write in this line will automatically exceute as soon as we run this file
    processor=DataProcessor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESSED_DIR,CONFIG_PATH) ##object of class data prcoesser
    ##THIS CONFIGPATH POINTS TO CONFIG.YAML
    processor.process()





    




        








        



    





       
        







