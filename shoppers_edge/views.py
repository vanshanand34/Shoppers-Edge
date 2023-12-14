from django.shortcuts import render
from django.http import  JsonResponse
from django import forms
from django.urls import reverse
from .flipkart import myoutput
from .forms import shoppingform
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from celery import shared_task
import asyncio

# Create your views here.

async def your_view(request,s_item):
    output = await myoutput(s_item)
    return render(request,"shoppers_edge/display.html",{"output":output})

async def my_function(request):
    if 'item' in request.GET:
        searchitem = request.GET['item']
        data = {
            'redirect_url': "search/%s" %(str(searchitem))
        }
        return JsonResponse(data)

async def index(request):
    if request.method=="POST":
        form = shoppingform(request.POST)
        if form.is_valid() :
            item = form.cleaned_data["product"]
            output = await myoutput(item)
            return render(request,"shoppers_edge/display.html",{"output":output})
        else:
            return render(request,"shoppers_edge/index.html",{"form":form})
    else:
        return render(request,"shoppers_edge/index.html",{"form":shoppingform()})
    
