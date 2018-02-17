import os
import csv
import time
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
from sklearn.externals import joblib
from sklearn import preprocessing
from django.conf import settings
from . import svm
from .data_process import process
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, LabelSet, Label

def update_model():
    process()
    svm.train_and_save_model('DO')
    svm.train_and_save_model('NH3N')
    svm.train_and_save_model('PH')

def load_model(obj, method):
    model_path = os.path.join(settings.BASE_DIR, 'model')
    model_name = obj + '.model'
    model = joblib.load(os.path.join(model_path,method,model_name))
    return model

def load_data(path):
    readfile = open(path,'r')
    reader = csv.reader(readfile)
    lst = []
    for row in reader:
        num = np.round([eval(item) for item in row],3)
        lst.append(num)
    data = np.array(lst)    
    return data

def predict(model,x):
    result = model.predict(x)
    return result

def plot(pred,y):
    x = np.arange(len(pred))
    p = figure(tools="pan,zoom_in,zoom_out,reset,save", x_axis_label='samples', y_axis_label='mg/L', plot_width=800, plot_height=500)
    p.line(x, pred, legend=u'预测值', line_width=2, line_color="blue")
    p.line(x, y, legend=u'实际值', line_width=2, line_color="red")
    script, div = components(p)
    dic = {'script':script, 'div':div}
    return dic

def restore(data,obj):
    obj_lst = {'month':0,'DO':1,'NH3N':2,'PH':3}
    #m,d = time.strftime('%m-%d',time.localtime(time.time())).split('-')  
    dataname =  'mean_and_std.csv'       
    path = os.path.join(settings.BASE_DIR, 'data', dataname)
    mean_and_std = load_data(path)
    mean = mean_and_std[0][obj_lst[obj]]
    std = mean_and_std[1][obj_lst[obj]]
    return data * std + mean

def rmse(pred,real):
    length = len(pred)
    res = 0
    for i in range(0,length):
        res = res + np.square(pred[i] - real[i])
    res = np.sqrt(res/length)
    return np.round(res,2)

def cor(pred,real):   
    return np.round(np.corrcoef(pred,real)[0][1],2)

def accuracy(obj,pred,real):
    length = len(pred)
    res = 0
    if(obj=='PH'):
        limit = 0.3
    if(obj=='DO'):
        limit = 1
    if(obj=='CODMn'):
        limit = 0.5
    if(obj=='NH3N'):
        limit = 0.3
    for i in range(0,length):
        if(np.abs(pred[i] - real[i]) <= limit):
            res = res + 1
    return np.round(res/length*100,2)                        

def test(obj,method):
    feature = 6
    m,d = time.strftime('%m-%d',time.localtime(time.time())).split('-')  
    dataname =  m + '_' + d + '_' + obj + '_test_sets.csv'       
    path = os.path.join(settings.BASE_DIR, 'data', dataname)
    data = load_data(path)
    model = load_model(obj,method)
    x = data[:,0:feature]
    y = data[:,feature]
    pred = predict(model,x)
    pred = restore(pred,obj)
    y = restore(y,obj)
    dic = plot(pred,y)
    _rmse = rmse(pred,y)
    _cor = cor(pred,y)
    _acy = accuracy(obj,pred,y)
    res = {'rmse':_rmse,'cor':_cor,'acy':_acy,'dic':dic,'num':len(y)}
    return res


def return_result():
    update_model()
    DO = test('DO','SVM')
    NH3N = test('NH3N','SVM')
    PH = test('PH','SVM')
    res = {'DO':DO,'NH3N':NH3N,'PH':PH}
    return res


