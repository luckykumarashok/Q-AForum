from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from dblog.DblogViews.BlogView import  *  
        
def logout_user(request):
    logout(request)
    return render(request,'dblog/index.html',{})        