# -*- coding: utf-8 -*-
"""GBTC.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/115qAZ3wIX-P6aYaq-utBV8UlqdXclU4f
"""

import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
from sklearn.model_selection import KFold
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import GradientBoostingClassifier
from pathlib import Path

def run_model(select_sector):
    #import csv to dataframe
    df = pd.read_csv(Path('Data_Prep_Output/'+select_sector+'.csv'), 
    parse_dates=True, #defining date
    infer_datetime_format=True # unifi date format
    ).dropna()  # remove NULL values
    
    #clean data from unnecessary paramenter => unnamed, currency, ticker, sector columns from the DataFrame
    df=df.drop(columns=['Unnamed: 0', 'date_x','reportedCurrency','Sector','ticker']) 
    df['roi_boolean']= df['q_roi'] >0 
    df.replace({False: 0, True: 1}, inplace=True) #change from False/True to 0/1
    df=df.drop(columns='q_roi')  
    X,y = df.drop('roi_boolean',axis=1),df.roi_boolean
#Separating data to train and validation sets
    kf = KFold(n_splits=5,random_state=42,shuffle=True)
    for train_index,val_index in kf.split(X):
        X_train,X_val = X.iloc[train_index],X.iloc[val_index]
        y_train,y_val = y.iloc[train_index],y.iloc[val_index] 
    gb_model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.5, max_depth=10, random_state=0)
    gb_model.fit(X_train,y_train)
    classification_output=classification_report(y_val,gb_model.predict(X_val),output_dict=True)
    #X_test = df.drop('roi_boolean',axis=1).sample(n=1)
    #results=gb_model.predict(X_test)
    return pd.DataFrame(classification_output)



#upload from google
#from google.colab import files
#uploaded = files.upload()
##file_name = uploaded.keys()
#df= import_data('Finance')
#df=df.drop(columns=['Unnamed: 0.1','Unnamed: 0', 'date_x','reportedCurrency','Sector','ticker'])
'''
#import data from CSV
df = pd.read_csv(
    'Finance.csv', #defined name of the file to upload
    parse_dates=True, #defining date
    infer_datetime_format=True # unifi date format
    ).dropna()  # remove NULL values
#df=df.drop(columns=['Unnamed: 0.1','Unnamed: 0', 'date_x','reportedCurrency','Sector','ticker']) #adjustmend before getting clead data
#add roi_boolean parameter

df['roi_boolean']= df['q_roi'] >0 
df.replace({False: 0, True: 1}, inplace=True) #change from False/True to 0/1
df=df.drop(columns='q_roi')
#df

#Defining label
X,y = df.drop('roi_boolean',axis=1),df.roi_boolean
#Separating data to train and validation sets
kf = KFold(n_splits=5,random_state=42,shuffle=True)
for train_index,val_index in kf.split(X):
    X_train,X_val = X.iloc[train_index],X.iloc[val_index],
    y_train,y_val = y.iloc[train_index],y.iloc[val_index],

#Creating GB model
gb_model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.5, max_depth=10, random_state=0)#learning_rate=0.1)
#Get model parameters
#gb_model.get_params()

#model fit with data
gb_model.fit(X_train,y_train)
print(classification_report(y_val,gb_model.predict(X_val)))

#selecting one sample for testing prediction
X_test = df.drop('roi_boolean',axis=1).sample(n=1)

#Predicting data
results=gb_model.predict(X_test)
results
'''