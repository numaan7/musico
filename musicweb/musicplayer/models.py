from django.db import models
from django.contrib.auth.models import User



class Tags(models.Model):
    name=models.CharField(max_length=100,unique=True)
 
    def __str__(self):
        return self.name
# Create your models here.
class Artist(models.Model):
    url=models.SlugField(unique=True)
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to="uploads")
    
    date=models.DateTimeField(auto_now_add=True)
    desc=models.TextField()
    def __str__(self):
        return self.name
class Genre(models.Model):
    name=models.CharField(max_length=100,unique=True)
    
    def __str__(self):
        return self.name
class Song(models.Model):
    url=models.SlugField(unique=True)
    song_name=models.CharField(max_length=1000,unique=True)
    image=models.ImageField(upload_to="uploads")
    price=models.IntegerField(default=0)
    artist=models.ForeignKey(Artist,on_delete=models.CASCADE)
    genere=models.ForeignKey(Genre,on_delete=models.CASCADE)
    desc=models.TextField()
    song=models.FileField(upload_to='uploads/')
    tags=models.ManyToManyField(Tags,blank=True)
    user=models.ManyToManyField(User,blank=True)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.song_name)

    
class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField( max_length=254)
    subject=models.CharField(max_length=1000)
    desc=models.TextField()
    def __str__(self):
        return self.email
class Order(models.Model):
    order_id=models.CharField(max_length=100)
    product_id=models.IntegerField()
    product_name=models.ForeignKey(Song,on_delete=models.CASCADE)
    paid_amount=models.IntegerField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    signature=models.CharField(max_length=100,default='')
    paid=models.BooleanField(default=False)
    def __str__(self):
        return str(self.product_name.song_name)
    
class Blog(models.Model):
    url=models.SlugField(unique=True)
    title=models.CharField(max_length=1000,unique=True)
    image=models.ImageField(upload_to="uploads")
    
    Author=models.ForeignKey(User,on_delete=models.CASCADE)
    genere=models.ForeignKey(Genre,on_delete=models.CASCADE)
    body=models.TextField()
    tags=models.ManyToManyField(Tags,blank=True)
    publish=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now_add=True)
 

    def __str__(self):
        return str(self.title)
class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    is_parent=models.BooleanField(default=True)
    parent = models.ForeignKey('self',blank=True, on_delete=models.CASCADE,null=True, related_name='replies')

    def __str__(self):
        return self.text

class Newsletter(models.Model):
    email=models.EmailField(blank=True,unique=True)
    def __str__(self):
        return self.email