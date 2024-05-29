from django.db import models
from myschool.core_attrs import CoreAttrs

class Author(models.Model, CoreAttrs):
    name = models.CharField(max_length=100)
    biography = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model, CoreAttrs):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13)
    genre = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    def list_display(self):
        return ['title','author','published_date','isbn','genre']
    def list_filter(self):
        return ['title']
    

class Member(models.Model, CoreAttrs):
    name = models.CharField(max_length=100, help_text='Enter user registration code')
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.name

    def list_display(self):
        return ['name','email','address']
    
    def list_filter(self):
        return ['name']
    

class Loan(models.Model, CoreAttrs):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(blank=True, null=True)
    is_returned = models.BooleanField(default=False, choices=[(True, 'Yes'),(False,'No')])

    def __str__(self):
        return f"{self.member.name}'s loan of {self.book.title}"
    
    def list_display(self):
        return ['book','member','return_date']

class Reservation(models.Model, CoreAttrs):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    reservation_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True, choices=[(True, "Active"), (False, "Not Active")])

    def __str__(self):
        return f"{self.member.name}'s reservation of {self.book.title}"
    def list_display(self):
        return ['book','member','reservation_date','is_active']
