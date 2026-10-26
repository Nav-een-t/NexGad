from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.
def index(request):
    h_category, _ = Category.objects.get_or_create(category="Headphone")
    e_category, _ = Category.objects.get_or_create(category="Ear Buds")
    s_category, _ = Category.objects.get_or_create(category="Speaker")
    head_phone = Product.objects.filter(category=h_category)
    ear_bud = Product.objects.filter(category=e_category)
    spea_ker = Product.objects.filter(category=s_category)
    head = {"head": Product.objects.all()[:3], "h_count": head_phone.count(), "e_count": ear_bud.count(), "s_count": spea_ker.count()}
    return render(request, "index.html", head)


def headphone(request):
    category=Category.objects.get(category='Headphone')
    product=Product.objects.filter(category=category)
    count=product.count()
    return render(request,'Shopall.html',{'product':product, 'count':count})

def earbud(request):
    category=Category.objects.get(category='Ear Buds')
    product=Product.objects.filter(category=category)
    count=product.count()
    return render(request,'Shopall.html',{'product':product, 'count':count})

def speaker(request):
    category=Category.objects.get(category='Speaker')
    product=Product.objects.filter(category=category)
    count=product.count()
    
    return render(request,'Shopall.html',{'product':product,'count':count})


from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import AuthenticationForm

@ensure_csrf_cookie
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Logged in as {user.get_username()}')
            return redirect('Home')
    else:
        form = AuthenticationForm()

    return render(request, 'Login.html', {
        'form': form,
        'hide_nav': True,
    })


from django.contrib import messages
from .forms import createUser

def userRegister(request):
    if request.method=='POST':
        form=createUser(request.POST)
        if form.is_valid():
            form.save()
            user_name=form.cleaned_data.get('username')
            messages.success(request,f'Account Created for {user_name} Successfully')
            return redirect('Login')
        
    else:
        form=createUser()
    return render(request,'SignUp.html',{'form':form, 'hide_nav':True})

from django.contrib.auth import logout
def Log_out(request):
    logout(request)
    messages.success(request,'Logout Successfully')
    return redirect(index)


def ProfileForm(request):
    user,created=Profile.objects.get_or_create(user=request.user)
    profile_pic_name=request.user.first_name[:1]
    if request.method=='POST':
        pic=request.FILES.get('pic')
        phone=request.POST.get('phone')
        bio=request.POST.get('bio')
        
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        
        request.user.first_name=first_name
        request.user.last_name=last_name
        request.user.save()

        user.phone=phone
        user.bio=bio
        if pic:
            user.image=pic
        user.save()
        
        return redirect('profile_page')
    return render(request,'ProfileForm.html',{'profile':user,'profile_pic':profile_pic_name})

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    order_item=Order.objects.filter(user=request.user)
    order_data=[]
    grand_total = 0
    for i in order_item:
        item=OrderItem.objects.filter(order=i)
        total = 0
        for j in item:
            total += j.quantity * j.product.c_price
        grand_total += total
        
        order_data.append({
            'id':i.id,
            'date_time':i.date_time,
            'items':item,
            'total':total,
            'address':i.address
        })
        
        
    count=order_item.count()
    
    orders = order_data[-4:][::-1]
    
    profile_pic_name=request.user.first_name[:1]
    
    return render(request,'Profile.html',{'profile':profile,'profile_pic':profile_pic_name,'orders':orders,'grand_total':grand_total,'count':count})

def cart_s(request, id):
    product = Product.objects.get(pk=id)
    cart_item, created = Cart.objects.get_or_create(product=product,user=request.user)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_page')

@login_required
def cart_page(request):
    items = Cart.objects.filter(user=request.user)
    total = 0
    for i in items:
        total += i.total_price()
    count=items.count()
    return render(request, 'Cart.html',{
        'items':items,
        'total':total,
        'count':count
        })

def inc(request, id):
    product = Product.objects.get(pk=id)
    cart_item, created = Cart.objects.get_or_create(product=product,user=request.user)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_page')

def dec(request, id):
    product = Product.objects.get(pk=id)
    cart_item, created = Cart.objects.get_or_create(product=product,user=request.user)
    
    if not created:
        cart_item.quantity -= 1
        cart_item.save()
        if cart_item.quantity == 0:
            cart_item.delete()

    return redirect('cart_page')

@login_required
def order(request):
    order_item=Order.objects.filter(user=request.user)
    order_data=[]
    grand_total = 0
    for i in order_item:
        item=OrderItem.objects.filter(order=i)
        total = 0
        for j in item:
            total += j.quantity * j.product.c_price
        grand_total += total
        
        order_data.append({
            'id':i.id,
            'date_time':i.date_time,
            'items':item,
            'total':total,
            'address':i.address
        })
        
        
    count=order_item.count()
    orders = order_data[::-1]
    return render(request,'Orders.html',{
        'orders':orders,
        'grand_total':grand_total,
        'count':count})

def all_items(request):
    query=request.GET.get('q')
    product=Product.objects.all()
    filteredProduct=None
    count=product.count()
    if query == '':
        return redirect(index)
    if query:
        filteredProduct=Product.objects.filter(
            c_desc__icontains=query
        ) | Product.objects.filter(
            name__icontains=query
        )
    else:
        filteredProduct = Product.objects.all()
    q_count=filteredProduct.count()
    return render(request,'Shopall.html', {'data':filteredProduct, 'query':query, 'product':product,'count':count,'q_count':q_count})



def product_details(request,id):
    product = Product.objects.get(pk=id)

    wished = False
    
    if request.user.is_authenticated:
        wished = Wishlist.objects.filter(product=product,user=request.user)
    
    return render(request,'Details.html',{'products':product, 'wished':wished})

def boat_fil(request):
    boat=Product.objects.get(name__icontains='boat rockerz 413')
    return render(request,'Details.html',{'products':boat})

def address(request,id=None):
    
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        phone=request.POST['phone']
        alt_phone=request.POST['alt_phone']
        addres=request.POST['address']
        city=request.POST['city']
        pin=request.POST['pin_code']
        state=request.POST['state']
        landmark=request.POST['landmark']
        cod=request.POST['cod']
    
        address_obj=Address()
        address_obj.first_name=first_name
        address_obj.last_name=last_name
        address_obj.user=request.user
        address_obj.user=request.user
        address_obj.phone=phone
        address_obj.alt_phone=alt_phone
        address_obj.adress=addres
        address_obj.city=city
        address_obj.pin_code=pin
        address_obj.state=state
        address_obj.land_mark=landmark
        address_obj.payment=cod
    
        address_obj.save()
        
        if id is not None:

            item = Cart.objects.get(pk=id)
            
            order = Order()
            order.user=request.user
            order.address=address_obj
            order.save()
            
            order_item = OrderItem()
            order_item.order=order
            order_item.product=item.product
            order_item.quantity=item.quantity
            order_item.save()
            
            item.delete()

        else:
            cart_items = Cart.objects.filter(user=request.user)
            order = Order()
            order.user=request.user
            order.address=address_obj
            order.save()

            for item in cart_items:
                order_item = OrderItem()
                order_item.order=order
                order_item.product=item.product
                order_item.quantity=item.quantity
                order_item.save()
            cart_items.delete()
            
        head = {
            'head': Product.objects.all()[:4],
            'ordered': True
        }

        return render(request,'index.html',head)

    return render(request,'Address.html',{'product_id': id})
        
def place_order(request, id=None):
    cart_item=Cart.objects.filter(user=request.user)
    if not cart_item.exists():
        return render(request,'Cart.html',{'order_error':True})
        
    if id is not None:
        return redirect('Address', id=id)

    return redirect('Address')

def about(request):
    return render(request,'About.html')

def contact(request):
    if  request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        
        contact = Contact()
        contact.user = request.user
        contact.first_name = first_name
        contact.last_name = last_name
        contact.email = email
        contact.subject = subject
        contact.message = message
        contact.save()
        messages.success(request,f'Message sent Successfully')
        return redirect('Home')
    return render(request,'Contact.html')

def cart_delete(request,id):
    cart_item = Cart.objects.get(pk=id)
    cart_item.delete()
    return redirect('cart_page')

@login_required
def wish(request,id):
    product = Product.objects.get(pk=id)
    item = Wishlist.objects.filter(product=product, user=request.user)
    if item.exists():
        item.delete()
    else:
        wishlist = Wishlist()
        wishlist.product = product
        wishlist.user = request.user
        wishlist.save()
        
    return redirect('Details',id=id)

@login_required
def wishlist(request):
    wishlist_items=Wishlist.objects.filter(user=request.user)
    count = wishlist_items.count()
    return render(request,'Wishlist.html',{'wish':wishlist_items,'count':count})
import os
import secrets

from django.conf import settings
from django.core.management import call_command
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST



@csrf_exempt
@require_POST
def import_products_once(request):
    expected_token = os.environ.get("PRODUCT_IMPORT_TOKEN", "")
    supplied_token = request.headers.get("X-Product-Import-Token", "")

    if not expected_token or not secrets.compare_digest(
        supplied_token, expected_token
    ):
        return HttpResponseForbidden("Invalid token")

    fixture_path = (
        settings.BASE_DIR / "napp" / "fixtures" / "nexad_products.json"
    )

    if not fixture_path.is_file():
        return HttpResponse("Fixture file not found", status=500)

    import json
    from django.db import transaction
    from .models import Category, Product

    try:
        with open(fixture_path, encoding="utf-8") as fixture_file:
            records = json.load(fixture_file)

        categories = {}
        for record in records:
            if record.get("model") != "napp.category":
                continue

            fields = record["fields"]
            category, _ = Category.objects.get_or_create(
                category=fields["category"]
            )
            categories[record["pk"]] = category

        added = 0
        updated = 0

        with transaction.atomic():
            for record in records:
                if record.get("model") != "napp.product":
                    continue

                fields = record["fields"]
                category = categories.get(fields["category"])

                if category is None:
                    raise ValueError("A product category is missing.")

                product = Product.objects.filter(
                    name=fields["name"]
                ).first()

                if product is None:
                    Product.objects.create(
                        category=category,
                        name=fields["name"],
                        c_image=fields["c_image"],
                        hover_image=fields.get("hover_image"),
                        c_desc=fields["c_desc"],
                        c_price=fields["c_price"],
                    )
                    added += 1
                else:
                    updated += 1

        return HttpResponse(
            f"Import completed. Added: {added}; already present: {updated}."
        )

    except Exception:
        return HttpResponse(
            "Import failed. Check Render logs before retrying.", status=500
        )
