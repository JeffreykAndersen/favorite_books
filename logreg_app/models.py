from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #regex email format

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name is Required."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name is Required."
        # email validator and database check
        if len(postData['email'])< 1:
             errors['email'] = "Email is required."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email!"
        existing_email = self.filter(email=postData['email'])
        if existing_email:
            errors['email'] = "Email already in use."
        # password validation and match
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if postData['confirm_pw'] != postData['password']:
            errors['confirm'] = "Passwords do not match."
        return errors
    
    def register(self, postData):
        hashed_password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()
        User.objects.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData['email'],
            password = hashed_password
        )

    def log_authenticate(self, email, password):
        users_with_email = self.filter(email=email)
        if not users_with_email:
            return False
        user=users_with_email[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())
    

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)
    objects =UserManager()

class BookManager(models.Manager):
    
    def book_validator(self, postData):
        errors ={}
        if len(postData['title']) < 1:
            errors['title'] = "Title is required."
        if len(postData['desc'])< 5:
            errors['desc'] ="Please be more descriptive"
        existing_book = self.filter(title = postData['title'])
        if existing_book:
            errors['exist'] ="Your favorite book is already here"
        return errors
    

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    created_by = models.ForeignKey(User, related_name="creator_of_book", on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(User,related_name="favorite_books")
    created_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)

    objects = BookManager()


