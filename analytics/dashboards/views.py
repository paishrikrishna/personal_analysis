from django.shortcuts import render,redirect
from django.template import loader  
from django.http import HttpResponse,JsonResponse
from dashboards.database_queires import firebase_actions
firebase_obj = firebase_actions("/home/RedBullAmgp/personal_analysis/analytics/dashboards/self-f70d2-firebase-adminsdk-5noxc-2b24c749dd.json")

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
        result.append({"date":date,"amount":amount})
    return JsonResponse({"data":result})
