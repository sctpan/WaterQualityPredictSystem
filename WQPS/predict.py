import time
import csv
import os
import numpy as np
from sklearn import preprocessing
from sklearn import decomposition
from .models import WaterQualityRecord 
from django.conf import settings
from sklearn.externals import joblib
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, LabelSet, Label

def get_last_months_data(loop=3):
    db = WaterQualityRecord.objects.order_by('station','year','month')
    year = db.values('year')
    month = db.values('month') 
    DO = db.values('DO')
    PH =  db.values('PH')
    NH3N = db.values('NH3N')
    length = len(month)
    data = []
    for i in range(length-loop,length):
        rcd = [month[i]['month'], DO[i]['DO'],NH3N[i]['NH3N'],PH[i]['PH'],year[i]['year']]
        data.append(rcd)
    data = np.array(data)
    return data

def load_data(path):
    readfile = open(path,'r')
    reader = csv.reader(readfile)
    lst = []
    for row in reader:
        num = np.round([eval(item) for item in row],3)
        lst.append(num)
    data = np.array(lst)    
    return data

def load_model(obj, method):
    model_path = os.path.join(settings.BASE_DIR, 'model')
    model_name = obj + '.model'
    model = joblib.load(os.path.join(model_path,method,model_name))
    return model

def build_x(data,obj):
    obj_lst = {'month':0,'DO':1,'NH3N':2,'PH':3}
    date = data[:,obj_lst['month']].T
    feature = data[:,obj_lst[obj]].T
    X = np.hstack((date,feature))
    return X.reshape(1,-1)

def standardize(data):
    scaler = preprocessing.StandardScaler().fit(data)
    data = scaler.transform(data)
    return data

def predict_next_month(obj,method):
    obj_lst = {'month':0,'DO':1,'NH3N':2,'PH':3}
    data = get_last_months_data()
    data = standardize(data)
    m,d = time.strftime('%m-%d',time.localtime(time.time())).split('-')  
    dataname = 'mean_and_std.csv'       
    path = os.path.join(settings.BASE_DIR, 'data', dataname)
    mean_and_std = load_data(path)
    mean = mean_and_std[0][obj_lst[obj]]
    std = mean_and_std[1][obj_lst[obj]]
    model = load_model(obj,method)
    result = model.predict(build_x(data,obj)) * std + mean
    return np.round(result[0],2)

def modify_month(m):
    if m < 10:
        m = '0' + str(m)
    else:
        m = str(m)
    return m

def plot(obj,method):
    obj_lst = {'month':0,'DO':1,'NH3N':2,'PH':3}
    pred = [predict_next_month(obj,method)]
    length = 6
    data = get_last_months_data(length)
    year = data[:,4]
    month = data[:,0]
    obj_data = data[:,obj_lst[obj]]
    date = []
    for i in range(0,length):
        m = modify_month(month[i])
        date.append(str(year[i]) + '-' + m)
    date = np.array(date, dtype=np.datetime64)
    pred_date = []
    if month[length-1] == 12:
        pred_date.append(str(year[length-1] + 1) + '-' + modify_month(1))
    else:
        pred_date.append(str(year[length-1]) + '-' + modify_month(month[length-1] + 1))
    pred_date = np.array(pred_date, dtype=np.datetime64)
    p = figure(tools="pan,hover,save", x_axis_type="datetime",x_axis_label='month', y_axis_label='mg/L',plot_width=800, plot_height=500)
    p.square(date, obj_data, fill_color="green", line_color="green",hover_color="red",size=12)
    p.line(date, obj_data, legend=u'历史数据', line_width=3,line_color="green")
    p.square(pred_date, pred, fill_color="blue", line_color="blue",hover_color="red",size=12)
    pred_date_for_dash_line = np.hstack((np.array(date[length-1]), pred_date))
    pred_for_dash_line = np.array([obj_data[length-1], pred[0]])
    p.line(pred_date_for_dash_line, pred_for_dash_line, legend=u'预测数据', line_dash='dashed', line_width=3, line_color="blue")
    script, div = components(p)
    dic = {'script':script, 'div':div}
    return dic

def return_pics():
    pred = [predict_next_month('DO','SVM'), predict_next_month('NH3N','SVM'), predict_next_month('PH','SVM')]
    pic = [plot('DO','SVM'),plot('NH3N','SVM'),plot('PH','SVM')]
    return {'pred':pred,'pic':pic}
