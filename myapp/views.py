from django.shortcuts import render, redirect
from .models import User, Contact, Product_clothes, Wishlist, Cart,Address, Transaction
from django.conf import settings
from django.core.mail import send_mail
import random
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from .models import Transaction
from .paytm import generate_checksum, verify_checksum

# Create your views here.

def index(request):
    try:
        user=User.objects.get(email=request.session['email'])
        if user.usertype=='seller':
            return redirect (seller_index)
        else:
            myproduct=Product_clothes.objects.all()            
            return render (request, "index.html", {'myproduct':myproduct})
    except:
        myproduct=Product_clothes.objects.all()            
        return render (request, "index.html", {'myproduct':myproduct})


def view_product(request, pk):
    wishlist_flag=False
    
    product=Product_clothes.objects.get(pk=pk)
    try:
        Wishlist.objects.get(product=product)
        wishlist_flag=True
    except:
        pass

    size=(product.product_size).split(",")
    color=(product.product_color).split(",")
    
    try:
        user=User.objects.get(email=request.session['email'])
        return render (request, 'view_product.html', {'product':product, 'user':user, 'color':color, 'size':size,'wishlist_flag':wishlist_flag })
    except: 
        return render (request, 'view_product.html', {'product':product,  'color':color, 'size':size,'wishlist_flag':wishlist_flag })


def seller_index(request):
    user=User.objects.get(email=request.session['email'])
    myproduct=Product_clothes.objects.filter(seller=user)
    man_wear, woman_wear, kid_wear= [], [], []
    man_wear=Product_clothes.objects.filter(product_category='man_wear') 
    woman_wear=Product_clothes.objects.filter(product_category='woman_wear') 
    kid_wear=Product_clothes.objects.filter(product_category='kid_wear') 
        
    arg={
        'myproduct':myproduct,
        'man_wear':man_wear,
        'woman_wear':woman_wear,
        'kid_wear':kid_wear,
             
    }
    return render (request, "seller_index.html", arg)



def seller_myproduct(request):
    user=User.objects.get(email=request.session['email'])
    myproduct=Product_clothes.objects.filter(seller=user)
    return render (request, 'seller_myproduct.html', {'myproduct':myproduct})

def seller_contact(request):
    return render (request, 'seller_contact.html')



def cart(request):
    try: 
        total_billing=0
        user=User.objects.get(email=request.session['email'])
        carts= Cart.objects.filter(user=user, payment_status='pending')
        for i in carts:
            total_billing+=i.total_prise
        return render(request, 'cart.html', {'carts':carts, 'total_billing':total_billing, 'total':total_billing+50})
    except:
        return render(request, 'login.html')


def checkout(request):
    total_billing=0
    user=User.objects.get(email=request.session['email'])
    carts=Cart.objects.filter(user=user, payment_status='pending')
    for i in carts:
        total_billing+=i.total_prise

    try:
        address=Address.objects.filter(user=user)
        return render(request, 'checkout.html',{'carts':carts, 'user':user, 'total_billing':total_billing, 'total':total_billing+50, 'address':address})
    except:
        return render(request, 'checkout.html',{'carts':carts, 'user':user, 'total_billing':total_billing, 'total':total_billing+50})


    
    
def contact(request):
    if request.method=='POST':
        try:
            Contact.objects.create(
                fname=request.POST['name'],
                email=request.POST['email'],
                subject=request.POST['subject'],
                message=request.POST['message'],
                image=request.FILES['image']
        )
        except:
                Contact.objects.create(
                fname=request.POST['name'],
                email=request.POST['email'],
                subject=request.POST['subject'],
                message=request.POST['message'],
        )
        msg='message sent successfully.'
        return render(request, 'contact.html', {'msg':msg})


    else:
        return render(request, 'contact.html')


def shop(request):
    product=Product_clothes.objects.all()
    return render(request, 'shop.html',{'product':product})

def logout(request):
    del request.session['email']
    del request.session['fname']
    del request.session['profile']
    del request.session['id']
    del request.session['wishlist_count']
    del request.session['carts_count']    

    return render(request, 'login.html')

        


def login(request):
    if request.method=='POST':
        try:

            user=User.objects.get(
                email=request.POST['email'], 
                password=request.POST['password']
            )

            request.session['email']=user.email
            request.session['fname']=user.fname
            request.session['profile']=user.profile.url
            request.session['id']=user.id    
            wishlist_product=Wishlist.objects.filter(seller=user)
            carts_product=Cart.objects.filter(user=user, payment_status='pending')
            request.session['carts_count']=len(carts_product)    

            request.session['wishlist_count']=len(wishlist_product)    
            

            if user.usertype=='user':
                return redirect (index)
            else:
                return redirect(seller_index)

        except:
            msg='Email or password are incorrect.'
            return render(request, 'login.html', {'msg':msg})
    else:
        return render(request, 'login.html')

def signup(request):
    if request.method=='POST':
        try:
            User.objects.get(email=request.POST['email'])
            msg='Email is already registered.'
            return render (request, 'signup.html', {'msg':msg})
            
        except:
            if request.POST['password']==request.POST['cpassword']:
                User.objects.create(
                fname=request.POST['fname'],
                lname=request.POST['lname'],
                email=request.POST['email'],
                mobile=request.POST['mobile'],
                city=request.POST['city'],
                profile=request.FILES['profile'],
                password=request.POST['password'],
                usertype=request.POST['usertype'])
                msg='Signup Successfully'
                return render (request, 'login.html', {'msg':msg})
            
            else:
                msg='Password and Cofirm password is not same.'
                return render (request, 'signup.html', {'msg':msg})


    else:   
        return render(request, 'signup.html')

def forgot_password(request):
    if request.method=='POST':
        try:        
            user=User.objects.get(email=request.POST['email'])
            otp=random.randrange(1000,9999)
            send_mail('send OTP', f'Your otp is {otp} for forgot password.',settings.EMAIL_HOST_USER, [user.email])
            return render(request, 'otp_verify.html', {'otp':otp, 'email':user.email })
        except:
            msg='Email is not registered.'
            return render(request, 'forgot_password.html', {'msg':msg })

    else:
        return render(request, 'forgot_password.html')

def otp_verify(request):
    if request.method=='POST':
        otp=request.POST['otp']
        email=request.POST['email']
        if otp==request.POST['v_otp']:

            return render(request, 'create_password.html', {'email':email})
        else:
            msg='please enter valid otp.'
            return render(request, 'otp_verify.html', {'msg':msg, 'otp':otp})

    else:
        return render(request, 'otp.html')



def create_password(request):
    if request.method=='POST':

        user=User.objects.get(email=request.POST['email'])
        if request.POST['new_password']==request.POST['cnew_password']:
            user.password=request.POST['new_password']
            user.save()
            msg='Your Password has been changed.'
            return render(request, 'login.html', {'msg':msg})
        else:
            msg='Password and Cofirm Password is not matched.'
            return render(request, 'create_password.html', {'msg':msg,'email':user.email })

    else:
        return render(request, 'create_password.html')



def change_password(request):
    if request.method=='POST':
        
        user=User.objects.get(email=request.POST['email'])
        if user.password==request.POST['old_password']:
            if request.POST['new_password']==request.POST['cnew_password']:
                user.password=request.POST['new_password']
                user.save()
                
                return redirect(logout)
            else:
                msg='Password and Confirm Password is not matched.'
                return render(request, 'change_password.html', {'msg':msg})

        else:
            msg='Please enter correct corrent password.'
            return render(request, 'change_password.html',{'msg':msg})
    else:
        return render(request, 'change_password.html')



def user_profile(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=='POST':
        user.fname=request.POST['fname']
        user.lname=request.POST['lname']
        user.mobile=request.POST['mobile']
        user.city=request.POST['city']
        
        try:
            user.profile=request.FILES['profile']
        except:
            pass
        user.save()
        request.session['fname']=user.fname
        request.session['profile']=user.profile.url
        msg='Profile updated Successfully.'

        if user.usertype=='seller':
            return render(request, 'profile.html', {'msg':msg,'user':user})
        else:
            return render(request, 'user_profile.html', {'msg':msg,'user':user})

    else:
        if user.usertype=='seller':
            return render(request, 'profile.html', {'user':user})
        else:
            return render(request, 'user_profile.html', {'user':user})

def seller_product_profile(request, pk):
    product=Product_clothes.objects.get(pk=pk)
    size=(product.product_size).split(",")
    color=(product.product_color).split(",")
 
    return render (request, 'seller_product_profile.html', {'product':product, 'color':color, 'size':size, })


def delete_product(request, pk):
    Product_clothes.objects.get(pk=pk).delete()

    return redirect (seller_myproduct)


def seller_edit_product(request, pk):
    product=Product_clothes.objects.get(pk=pk)
    
    if request.method=='POST':
        color=request.POST.getlist('product_color')
        product_color=""
        for i in color:
            product_color=product_color+","+i 

        size=request.POST.getlist('product_size')        
        product_size=""
        for i in size:
            product_size=product_size+","+i

        product.product_category=request.POST['product_category']
        product.product_name=request.POST['product_name']
        product.product_prise=request.POST['product_prise']
        product.product_discount=request.POST['product_discount']
        product.product_discs=request.POST['product_disc']

        product.product_cprise=int(request.POST['product_prise'])*(100-int(request.POST['product_discount']))/100       
        product.product_size=product_size[1:]       
        product.product_color=product_color[1:]
        try:
            product.product_image=request.FILES['product_image'],
        except:
            pass
        product.save()
        p_size=(product.product_size).split(",")
        p_color=(product.product_color).split(",")
        size=['XS','S','M','L', 'XL']
        color=['BLACK','RED','WHITE','BLUE', 'GREEN']
        msg='Product updated successfully.'        
        return render (request, 'seller_edit_product.html', {'msg':msg,'product':product,'color':color, 'size':size, 'p_size':p_size,'p_color':p_color})
                    
    else:   
    
        p_size=(product.product_size).split(",")
        p_color=(product.product_color).split(",")
        size=['XS','S','M','L', 'XL']
        color=['BLACK','RED','WHITE','BLUE', 'GREEN']
        return render (request, 'seller_edit_product.html', {'product':product,'color':color, 'size':size, 'p_size':p_size,'p_color':p_color})




def seller_add_product(request):
    email=request.session['email']
    user=User.objects.get(email=email)
    if request.method=='POST':
        color=request.POST.getlist('product_color')
        product_color=""
        for i in color:
            product_color=product_color+","+i 

        size=request.POST.getlist('product_size')        
        product_size=""
        for i in size:
            product_size=product_size+","+i

        Product_clothes.objects.create(
        seller=user,
        product_category=request.POST['product_category'],
        product_name=request.POST['product_name'],       
        product_prise=request.POST['product_prise'],
        product_discount=request.POST['product_discount'],       
        product_cprise=(int(request.POST['product_prise'])*(100-int(request.POST['product_discount']))/100),       
        product_size=product_size[1:],       
        product_color=product_color[1:],
        product_disc=request.POST['product_disc'],       
        product_image=request.FILES['product_image'],       
             )
        msg='Product added successfully.'
        return render(request, 'seller_add_product.html', {'msg':msg})
            
        
    else:
        size=['XS','S','M','L', 'XL']
        color=['BLACK','RED','WHITE','BLUE', 'GREEN']        
        return render(request, 'seller_add_product.html', {'size':size, 'color':color})


def by_category(request,pc):
    
    myproduct=Product_clothes.objects.filter(product_category=pc)

    if len(myproduct)==0:
        myproduct=Product_clothes.objects.all()

    return render(request, 'shop.html', {'myproduct':myproduct, 'pc':pc})



    

def wishlist(request):

    try:
        user=User.objects.get(email=request.session['email'])
        if request.session['email']:
            wishlist_product=Wishlist.objects.filter(seller=user)
            return render(request, 'add_to_wishlist.html', {'wishlist_product':wishlist_product})
    except:
        return render(request, 'login.html', {'msg': 'Please login First.'})

def add_to_wishlist(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product_clothes.objects.get(pk=pk)
    
    Wishlist.objects.create(
                seller=user,
                product=product
                )
    wishlist_product=Wishlist.objects.filter(seller=user)
    request.session['wishlist_count']=len(wishlist_product)

    return redirect ('wishlist')


def remove_from_wishlist(request, pk):
    user=User.objects.get(email=request.session['email'])
    product=Product_clothes.objects.get(pk=pk)
    wishlist_product=Wishlist.objects.filter(seller=user)
    Wishlist.objects.get(product=product, seller=user).delete()
    request.session['wishlist_count']=len(wishlist_product)
    return redirect(wishlist) 

def add_to_cart(request,pk):
    try:
        user=User.objects.get(email=request.session['email'])
        product=Product_clothes.objects.get(pk=pk)
        try:
            Cart.objects.get(user=user, product=product, payment_status='pending')

        except:    
            Cart.objects.create(
            user=user,
            product=product,
            total_prise=product.product_cprise
            )
        carts_count=Cart.objects.filter(user=user, payment_status='pending')
        request.session['carts_count']=len(carts_count)    

        return redirect(shop)
 
    except:
        return render (request,'login.html')

    
def remove_from_cart(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product_clothes.objects.get(pk=pk)
    Cart.objects.get(user=user, product=product, payment_status='pending').delete()
    carts_count=Cart.objects.filter(user=user, payment_status='pending')
    request.session['carts_count']=len(carts_count)    
    return redirect(cart)


def change_qty(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product_clothes.objects.get(pk=pk)
    carts=Cart.objects.get(user=user, product=product)
    s=request.POST['product_qty']
    carts.product_qty=int(s)
    carts.total_prise=int(s)*product.product_cprise
    carts.save()
    
    return redirect(cart)

def add_address(request):
    user=User.objects.get(email=request.session['email'])
    Address.objects.create(
        user=user,
        address_1=request.POST['address_1'],
        address_2=request.POST['address_2'],
        city=request.POST['city'],
        state=request.POST['state'],
        zipcode=request.POST['zipcode'],
        contry=request.POST['contry'],
    )
    return redirect(checkout)

def remove_address(request,apk):
    user=User.objects.get(email=request.session['email'])
    address=Address.objects.get(pk=apk)
    address.delete()
    return redirect(checkout)


def pay(request):
    if request.method=='POST':
        amount=request.POST['payable_amount']
    user=User.objects.get(email=request.session['email'])
    transaction = Transaction.objects.create(made_by=user, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', user.email),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)
    print(checksum)
    transaction.checksum = checksum
    
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    carts=Cart.objects.filter(user=user,payment_status='pending')
    for cart in carts:
        cart.payment_status='paid'
        cart.save()
    
    carts=Cart.objects.filter(user=user,payment_status='pending')
    request.session['carts_count']=len(carts)    

    return render(request, 'redirect.html', context=paytm_params)


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        

        return render(request, 'callback.html', context=received_data)


def myorder(request): 
    user=User.objects.get(email=request.session['email'])
    myorder=Cart.objects.filter(user=user,payment_status='paid')
    return render(request, 'myorder.html', {'myorder':myorder})