# -*- coding: utf-8 -*-
import time
import csv
import os
import numpy as np
from sklearn import preprocessing
from sklearn import decomposition
from .models import WaterQualityRecord 
from django.conf import settings

def load_data():
    db = WaterQualityRecord.objects.order_by('station','year','month')
    month = db.values('month') 
    DO = db.values('DO')
    PH =  db.values('PH')
    NH3N = db.values('NH3N')
    length = len(month)
    data = []
    for i in range(0,length):
        rcd = [month[i]['month'], DO[i]['DO'],NH3N[i]['NH3N'],PH[i]['PH']]
        data.append(rcd)
    data = np.array(data)
    return data

def select_Y(data,feature_num):
    feature_num = feature_num - 1
    Y = np.ones(len(data)).reshape(len(data),1)
    for i in range(0,len(data)):
        Y[i] = data[i][feature_num]
    return Y

def select_X(data,feature_lst):
    X = select_Y(data,feature_lst[0])
    for i in range(1,len(feature_lst)):
        X = np.hstack((X,select_Y(data,feature_lst[i])))
    return X
        
def loop_feature(data,feature_num,loop):
    feature = select_Y(data,feature_num)
    length = len(feature)
    looped_feature = np.ones([loop,length-loop])
    for i in range(0,length-loop):
        for j in range(0,loop):
            looped_feature[j][i] = feature[i+j]
    return looped_feature.T

def build_sets_has_loop(filename,obj_num,feature_num,loop_feature_num,loop):
    data = load_data(filename)
    length = len(data)    
    Y = select_Y(data,obj_num)
    Y = Y[loop:length,:] 
    X = select_X(data,feature_num)
    X = X[loop:length,:]
    looped_feature = loop_feature(data,loop_feature_num,loop)
    sets = np.hstack((X,looped_feature,Y))
    return sets

def build_training_set(sets,percent):
    length = int(len(sets) * percent)
    return sets[0:length,:]

def build_test_set(sets,percent):
    length = int(len(sets) * (1-percent))
    return sets[length:len(sets),:]

def write_set(path,obj,sets,mode):
    filename = path
    if(mode == 1):
        filename = filename + obj + '_training_sets.csv'
    else:
        filename = filename + obj + '_test_sets.csv'
    np.savetxt(filename,sets,delimiter=',')
    
def do_pca(data,num):
    pca = decomposition.PCA(n_components=num)
    after_pca_data = pca.fit_transform(data)
    return after_pca_data

def standardize(data):
    scaler = preprocessing.StandardScaler().fit(data)
    data = scaler.transform(data)
    return data

def remove_cross_station(data,loop):
    res = data[0:84-loop,:]
    for i in range(1,8):
        res = np.vstack((res,data[i*84:i*84+84-loop,:]))
    return res

def generate_sets(data,obj,loop=3):
    m,d = time.strftime('%m-%d',time.localtime(time.time())).split('-')  
    date =  m + '_' + d + '_'
    write_dir_path = os.path.join(settings.BASE_DIR, 'data', date)
    obj_lst = {'month':1,'DO':2,'NH3N':3,'PH':4}
    obj_num = obj_lst[obj]
    month = loop_feature(data,obj_lst['month'],loop)
    X = loop_feature(data,obj_num,loop)
    Y = select_Y(data,obj_num)
    length = len(data) 
    Y = Y[loop:length,:] 
    sets = np.hstack((month,X,Y))
    sets = remove_cross_station(sets,loop)
    training_set = build_training_set(sets,0.8)
    test_set = build_test_set(sets,0.2)
    write_set(write_dir_path,obj,training_set,1)
    write_set(write_dir_path,obj,test_set,2)

def save_mean_and_std(data):
    scaler = preprocessing.StandardScaler().fit(data)
    mean_and_std = np.vstack((scaler.mean_,np.sqrt(scaler.var_)))
    m,d = time.strftime('%m-%d',time.localtime(time.time())).split('-')  
    date =  m + '_' + d + '_'
    write_dir_path = os.path.join(settings.BASE_DIR, 'data', date)
    filename = write_dir_path + 'mean_and_std.csv'
    np.savetxt(filename,mean_and_std,delimiter=',')

def process():
    data = load_data()
    save_mean_and_std(data)
    data = standardize(data)    
    generate_sets(data,'DO')
    generate_sets(data,'NH3N')
    generate_sets(data,'PH')
















    