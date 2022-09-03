from django.shortcuts import render,redirect
from django.template import loader  
from django.http import HttpResponse,JsonResponse
from dashboards.database_queires import firebase_actions
from dashboards.gmail_reader import *
from dashboards.keen_dashboard import keen_dashboard_queries


sample_data = keen_dashboard_queries()
firebase_obj = firebase_actions("/home/shripais003/personal_analysis/analytics/dashboards/self-f70d2-firebase-adminsdk-5noxc-2b24c749dd.json")
month = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
# Create your views here.

def home_page(request):
    template = loader.get_template('home_page.html') 
    return HttpResponse(template.render())  


def login(request):
    if request.GET['login'] == "true":
        template = loader.get_template('home_page.html') 
    else:
        template = loader.get_template('login.html') 
    return HttpResponse(template.render())



def day_wise_transactions(request):
    data = firebase_obj.day_wise_transactions()
    return JsonResponse({'days':list(data.keys()),'amount':list(data.values())})

def day_wise_json(request):
    data = firebase_obj.day_wise_transactions()
    result = []
    for (date,amount) in data.items():
        result.append({"date":date.split(" ")[0],"time":date.split(" ")[1],"amount":amount,"date_order_num":int(date.split("-")[1]+date.split("-")[0]+date.split(" ")[1].replace(":","")),"month_aplh":month[int(date.split("-")[1])-1]})
    return JsonResponse({"data":result})

def receiver_wise_json(request):
    data = firebase_obj.receiver_wise_transactions()
    result = []
    for (receiver,amount) in data.items():
        result.append({"receiver":receiver,"amount":amount})
    return JsonResponse({"data":result})


def credit_data_refresh(request):
    credit_card_emails(firebase_obj)
    return JsonResponse({"status":200})


def update_dashboards(request):
    data = firebase_obj.day_wise_transactions()
    sample_data.push_data_lsit("Credit_Day_wise_Transactions",data)
    return JsonResponse({"status":200})


