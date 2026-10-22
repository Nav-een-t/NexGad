from django.db import models

# Create your models here.

class Category(models.Model):
    category=models.CharField(max_length=100)
    def __str__(self):
        return self.category
    
    
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100, default='Product')
    c_image=models.ImageField(upload_to='products')
    hover_image=models.ImageField(upload_to='products',null=True, blank=True)
    c_desc=models.TextField(max_length=500)
    c_price=models.IntegerField()
    
    

from django.contrib.auth.models import User
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='Profile',null=True, blank=True)
    phone=models.CharField(max_length=14,blank=True,null=True)
    bio=models.TextField(max_length=500,default='No bio added yet')
    
    def __str__(self):
        return self.user.username
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    
    def total_price(self):
        return self.quantity * self.product.c_price

class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=150)
    last_name=models.CharField(max_length=150)
    phone=models.IntegerField()
    alt_phone=models.IntegerField()
    adress=models.TextField(max_length=250)
    city=models.CharField(max_length=50)
    pin_code = models.CharField(max_length=6)
    state=models.CharField(max_length=100)
    land_mark=models.TextField(max_length=250,null=True,blank=True)
    payment = models.CharField(max_length=20, default='COD')

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address,on_delete=models.CASCADE,null=True, blank=True)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    
class Contact(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=400)
    message = models.TextField()
    
class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)