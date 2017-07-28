"""
Name: Jessica Kam
Date: 2017/07/25
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, Imputer, LabelEncoder, OneHotEncoder

class DataPreprocessing():
    def __init__(self):
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.X = None
        self.y = None
    
    def importDataset(self, dataset_name, X_start_index=0, X_end_index=-1, y_index=-1):
        dataset = pd.read_csv(dataset_name)
        self.X = dataset.iloc[:, X_start_index:X_end_index].values
        self.y = dataset.iloc[:, y_index].values
    
    def fillInMissingData(self, filler='NaN', strategy='mean', axis=0, index_start_fill=1, index_end_fill=3):
        imputer = Imputer(missing_values=filler, strategy=strategy, axis=axis, *args, **kwargs)
        imputer = imputer.fit(self.X[:, index_start_fill:index_end_fill])
        self.X[:, index_start_fill: index_end_fill] = imputer.transform(self.X[:, index_start_fill:index_end_fill])
    
    def encodeCategoricalDataForIndependentVar(self, column_to_encode=0):
        labelencoder_X = LabelEncoder()
        self.X[:, column_to_encode] = labelencoder_X.fit_transform(self.X[:, column_to_encode])
        onehotencoder = OneHotEncoder(categorical_features=[column_to_encode])
        self.X = onehotencoder.fit_transform(self.X).toarray()
    
    def encodeCategoricalDataForDependentVar(self):
        labelencoder_y = LabelEncoder()
        self.y = labelencoder_y.fit_transform(self.y)
    ###
    def avoidTheDummyVariableTrap(self, start_index=1):
        self.X = self.X[:, start_index:]
        
    def splitIntoTrainingAndTestSets(self, test_size=0.2, random_state=0, *args, **kwargs):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, *args, **kwargs) 
        
    def scaleFeatures(self):
        sc_X = StandardScaler()
        self.X_train = sc_X.fit_transform(self.X_train)
        self.X_test = sc_X.transform(self.X_test)
        sc_y = StandardScaler()
        self.y_train = sc_y.fit_transform(self.y_train)

