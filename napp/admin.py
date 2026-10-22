from django.contrib import admin
from .models import Category
from .models import Cart
class Cart_det(admin.ModelAdmin):
    list_display=('user','product','quantity')
from .models import Product
class Product_det(admin.ModelAdmin):
    list_display=('category','c_image','c_desc','c_price')
from .models import Profile
from .models import Order  
from .models import Address
from .models import OrderItem
from .models import Contact
from .models import Wishlist

# Register your models here.
admin.site.register(Category)
admin.site.register(Cart,Cart_det)
admin.site.register(Product,Product_det)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(OrderItem)
admin.site.register(Contact)
admin.site.register(Wishlist)