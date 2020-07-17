from django.urls import path
from . import views

urlpatterns = [
    path('', views.logreg),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('main', views.home)
]
