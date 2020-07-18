from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def logreg(request):
    return render(request, 'logreg.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                print(key, value)
            return redirect('/')
        else:
            User.objects.register(request.POST)
            user = User.objects.last()
            request.session['id'] = user.id
            request.session['user'] = user.first_name
            return redirect('/main')

def login(request):
    result = User.objects.log_authenticate(request.POST['user_email'], request.POST['user_password'])
    if result == False:
        return redirect('/')
    if result == True:
        user = User.objects.get(email=request.POST['user_email'])
        request.session['id'] = user.id
        request.session['user'] = user.first_name
        return redirect('/main')

def logout(request):
    request.session.flush()
    return redirect('/')

def home(request):
    if 'user' not in request.session:
        return redirect('/') 
    context = {
        "books": Book.objects.all()
    }
    return render(request, "home.html", context)

def add_book(request):
    if request.method =="POST":
        errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            print(key, value)
        return redirect ('/main')
    else:
        user = User.objects.get(id=request.session['id'])
        book = Book.objects.create(
            title = request.POST['title'],
            desc = request.POST['desc'],
            created_by = user
        )
        user.favorite_books.add(book)
        return redirect ('/main')

def edit(request, id):
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            print(key, value)
        return redirect('/book/'+str(id))
    edited_book = Book.objects.get(id=id)
    edited_book.title = request.POST['title']
    edited_book.desc = request.POST['desc']
    edited_book.save()
    return redirect('/main')

def book_page(request, id):
    if 'user' not in request.session:
        return redirect('/')
    context={
        "this_book" : Book.objects.get(id=id),
        "this_user": User.objects.get(id=request.session['id'])
    }
    return render(request, 'book.html', context)
    
