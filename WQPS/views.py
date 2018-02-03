import time
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .data_process import process
from .svm import train_and_save_model
from .predict import predict_next_month, return_pics
from .model_test import return_result

# Create your views here.
#@login_required
def index(request):
    #process()
    #train_and_save_model()
    #DO_predict = predict_next_month()
    flag = 1
    return render(request, 'index.html',{'flag':flag})
    #return render(request, 'index.html', {'DO_predict':DO_predict})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get("username", None)
        passwd = request.POST.get("passwd", None)
        user = authenticate(username=username, password=passwd) 
        if user:
            login(request,user)
            return redirect('/manage/')
    return render(request, 'index.html',{'flag':2})

def predict(request):
    y,m = time.strftime('%Y-%m',time.localtime(time.time())).split('-')
    res = return_pics()
    script = [res['pic'][0]['script'],res['pic'][1]['script'],res['pic'][2]['script']]
    div = [res['pic'][0]['div'],res['pic'][1]['div'],res['pic'][2]['div']]
    pred = res['pred']
    content = {'script':script,'div':div,'year':y, 'month':m, 'pred':pred}
    return render(request,'predict.html',content)

@login_required
def manage(request):
    username = request.user.get_username()
    return render(request, 'manage.html')

def model(request):
    res = return_result()
    script = [res['DO']['dic']['script'],res['NH3N']['dic']['script'],res['PH']['dic']['script']]
    div = [res['DO']['dic']['div'],res['NH3N']['dic']['div'],res['PH']['dic']['div']]
    num = res['DO']['num']
    rmse = [res['DO']['rmse'],res['NH3N']['rmse'],res['PH']['rmse']]
    acy =  [res['DO']['acy'],res['NH3N']['acy'],res['PH']['acy']]
    cor = [res['DO']['cor'],res['NH3N']['cor'],res['PH']['cor']]
    content = {'script':script,'div':div,'num':num,'rmse':rmse,'acy':acy,'cor':cor}
    return render(request, 'model.html', content)

def user_logout(request):
    logout(request)
    return redirect('/index/')

@login_required
def admin(request):
    return redirect('admin/')
   
