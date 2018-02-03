# -*- coding: utf-8 -*-
import os
import csv
import time
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
from sklearn.externals import joblib
from sklearn import preprocessing
from django.conf import settings

global PH_net
global DO_net
global CODMn_net
global NH3N_net
def load_data(path):
    readfile = open(path,'r')
    reader = csv.reader(readfile)
    lst = []
    for row in reader:
        num = np.round([eval(item) for item in row],3)
        lst.append(num)
    data = np.array(lst)    
    return data

def build_data(data,delay):
    length = data.size
    y = np.ones(length-delay)
    for i in range(0,length-delay):
        y[i] = data[i+delay]   
    x = np.ones([delay,length-delay])
    for i in range(0,length-delay):
        for j in range(0,delay):
            x[j][i] = data[i+j]
    return x.T,y

def train(DO_x,DO_y):  
    DO_net = SVR(kernel='rbf')
    DO_net.fit(DO_x,DO_y)   
    return DO_net

def predict(obj,input_data):  #接口
    result = []
    global PH_net
    global DO_net
    global CODMn_net
    global NH3N_net
    if(obj=='PH'):
        result = PH_net.predict(input_data)       
    if(obj=='DO'):
        result = DO_net.predict(input_data)          
    if(obj=='CODMn'):
        result = CODMn_net.predict(input_data) 
    if(obj=='NH3N'):
        result = NH3N_net.predict(input_data) 
    return result

def train_and_save_model(obj):
    feature = 6
    m,d = time.strftime('%m-%d',time.localtime(time.time())).split('-')  
    dataname =  m + '_' + d + '_' + obj + '_training_sets.csv'       
    path = os.path.join(settings.BASE_DIR, 'data', dataname)
    model_path = os.path.join(settings.BASE_DIR, 'model')
    model_name = obj + '.model'
    data = load_data(path)
    x = data[:,0:feature]
    y = data[:,feature]
    model = train(x,y)
    '''
    plt.figure(1)
    res = predict('DO',DO_x)
    plot(res,DO_y)
    DO_valid = predict('DO',DO_valid_x)
    np.savetxt(path + exp + 'svm_training_predict.csv',DO_valid,delimiter=',')
    '''
    joblib.dump(model, os.path.join(model_path,'SVM',model_name))

