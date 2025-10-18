###we give and define out model paramenter and our randomizes search cv parameters
from scipy.stats import randint,uniform

LIGHTGM_PARAMS={ ###refer light gbm documnetatiom, n ames should match with given in doc
    'n-estimators':randint(100,500), 
     'max_depth'  : randint(5,50),
     'learning_rate': uniform(0.01,0.2),
     'num_leaves': randint(20,100),
     'boosting_type':['gbdt','dart','goss'],
}   
## WE CAN ALSO DO GRID SIZE CV , BUT WILL TAKE LON TIME, RANDOMIZED SEACH CV DOES 
#FASTER##
RANDOM_SEARCH_PARAMS={
    'n_iter':4,
    'cv':2,
    'n_jobs':-1,
    'verbose':2,
    'random_state':42,
    'scoring':'accuracy'
}