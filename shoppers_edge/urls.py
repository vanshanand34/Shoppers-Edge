from django.urls import path
from . import views

urlpatterns = [
    path('home',views.index,name="index"),
    path('my_function', views.my_function , name="my_function"),
    path('search/<s_item>', views.your_view , name="searchitem")
]