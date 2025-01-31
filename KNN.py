#import all libraries
import talib as ta
import torch
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import io
from PIL import Image
from sklearn import datasets
from sklearn.metrics import accuracy_score
from scipy.io import loadmat
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import roc_auc_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score

#load data
Df= pd.read_csv('./data_loader/processed_data/spy_processed.csv')
Df=Df.dropna()

#choose target to be the movement of next day price
target = Df['ROC_1']
X = Df.drop(['ROC_1', 'Date', 'Volume', 'FSMA_10'], axis=1)

# normalize the data
sc_X = StandardScaler()
X= sc_X.fit_transform(X)
X_new = pd.DataFrame(data=X)
# set the context window size
window_size = 10

input_list = []
output_list = []
for idx, output in enumerate(target):
    if idx < window_size:
        continue
    input = X_new.iloc[range(idx-window_size, idx), :].to_numpy().ravel()
    input_list.append(input)
    output_list.append(output)

    dummy = 1

assert(len(input_list) == len(output_list))
X_new=pd.DataFrame(input_list)
target=pd.DataFrame(output_list)

target[target <= 0] = 0
target[target > 0] = 1


#split train test to 7:3
t=.7
split = int(t*len(X))

x_tr=X_new.iloc[:split]
x_te=X_new.iloc[split:]
y_tr=target.iloc[:split]
y_te=target.iloc[split:]

output=np.array(y_tr)
y_tr=output.ravel()



#set of parameters for random search
neighbours=[2,5,10,12,15,20,40,50,70,100]
parameters = {'n_neighbors': neighbours}

knn_g = KNeighborsClassifier()
knn_searched = RandomizedSearchCV(knn_g, parameters, cv = 5, n_iter = 5, verbose=0, n_jobs = -1)

knn_searched.fit(x_tr,y_tr)
print(knn_searched.best_params_)
knn_predict = knn_searched.best_estimator_
print(knn_predict.get_params)
knn_predict.fit(x_tr,y_tr)
knn_pred_tr = knn_predict.predict(x_tr)
#print train and validation accuracy
print("KNN training accuracy for next day", accuracy_score(y_tr, knn_pred_tr))
knn_pred_val = knn_predict.predict(x_te)
print("KNN testing accuracy for next day",accuracy_score(y_te, knn_pred_val))

#print f1 score
print("the f1 score for KNN next day prediction is", f1_score(y_te, knn_pred_val, average='binary'))


# the model below predicts the movement for 10 day average trends


#load data
Df= pd.read_csv('./data_loader/processed_data/spy_processed.csv')
Df=Df.dropna()

#choose target to be the average movement of next 10 day price
target = Df['FSMA_10']
X = Df.drop(['ROC_1', 'Date', 'Volume', 'FSMA_10'], axis=1)

# normalize the data
sc_X = StandardScaler()
X= sc_X.fit_transform(X)
X_new = pd.DataFrame(data=X)
# set the context window size

# set the context window size
window_size = 10

input_list = []
output_list = []
for idx, output in enumerate(target):
    if idx < window_size:
        continue
    input = X_new.iloc[range(idx-window_size, idx), :].to_numpy().ravel()
    input_list.append(input)
    output_list.append(output)

    dummy = 1

assert(len(input_list) == len(output_list))
X_new=pd.DataFrame(input_list)
target=pd.DataFrame(output_list)

target[target <= 0] = 0
target[target > 0] = 1


#split train test to 7:3
t=.7
split = int(t*len(X))

x_tr=X_new.iloc[:split]
x_te=X_new.iloc[split:]
y_tr=target.iloc[:split]
y_te=target.iloc[split:]

output=np.array(y_tr)
y_tr=output.ravel()
#set of parameters for random search
neighbours=[2,5,10,12,15,20, 40, 50,70,100]
parameters = {'n_neighbors': neighbours}

knn_g = KNeighborsClassifier()
knn_searched = RandomizedSearchCV(knn_g, parameters, cv = 5, n_iter = 5, verbose=0, n_jobs = -1)

knn_searched.fit(x_tr,y_tr)
print(knn_searched.best_params_)
knn_predict = knn_searched.best_estimator_
print(knn_predict.get_params)
knn_predict.fit(x_tr,y_tr)
knn_pred_tr = knn_predict.predict(x_tr)
#print train and validation accuracy
print("KNN training accuracy for 10 day average", accuracy_score(y_tr, knn_pred_tr))
knn_pred_val = knn_predict.predict(x_te)
print("KNN testing accuracy for 10 day average", accuracy_score(y_te, knn_pred_val))

#print f1 score
print("the f1 score for KNN 10 days average is", f1_score(y_te, knn_pred_val, average='binary'))
