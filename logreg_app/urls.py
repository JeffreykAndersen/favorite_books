from django.urls import path
from . import views

urlpatterns = [
    path('', views.logreg),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('main', views.home),
    path('add_book', views.add_book),
    path('book/<int:id>', views.book_page),
    path('edit/<int:id>', views.edit),
    path('like/<int:id>', views.like_book),
    path('unlike/<int:id>', views.unlike)
]
