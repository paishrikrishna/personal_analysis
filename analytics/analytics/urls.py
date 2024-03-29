"""analytics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dashboards.views import home_page,login,day_wise_transactions,day_wise_json,receiver_wise_json,credit_data_refresh,update_dashboards

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_page),
    path('login/',login),
    path('day_wise_transactions/',day_wise_transactions),
    path('day_wise_json/',day_wise_json),
    path('receiver_wise_json/',receiver_wise_json),
    path('credit_data_refresh/',credit_data_refresh),
    path('update_dashboards/',update_dashboards)
]
