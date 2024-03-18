import stripe
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import auth,messages
from django.contrib.auth import login
from django.contrib.auth import logout
from myapp.forms import ProductForm, customerreg, userreg
from myapp.models import Complaint, Pay, Payment, Product, CartItem,Review
from .forms import ComplaintForm, PaymentForm, ReviewForm
from django.shortcuts import render, get_object_or_404
from .models import  Paystatus, productss
from .models import Paymentz

def add_complaint(request):
        form=ComplaintForm()
        u=request.user
        print(u)
        if request.method == 'POST':
            form = ComplaintForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user=u
                obj.save()
                return redirect('complaint_success')
        return render(request, 'complaint.html', {'form': form})

def view_complaints(request):
    # Assuming customers are associated with users
    user_complaints = Complaint.objects.filter()
    return render(request, 'viewcomp.html', {'user_complaints': user_complaints})

def complaint_success(request):
    return render(request, 'complaint_success.html')

def home(request):
    return render(request,'index.html') 

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def blog(request):
    return render(request,'blog.html')

def shop(request):
    data=Product.objects.all()
    return render(request,'shop.html',{'data':data})

def add_product(request):
    form=ProductForm()
    if request.method=='POST':
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin')
    return render(request,'add_product.html',{"form":form})

def viewproduct(request):
    data=Product.objects.all()
    return render(request,'view_product.html',{'data':data})

def update_product(request,id):
    data=Product.objects.get(id=id)
    form=ProductForm(instance=data)
    if request.method=='POST':
        form=ProductForm(request.POST,request.FILES,instance=data)
        if form.is_valid():
            form.save()
            return redirect('viewproduct')
    return render(request,'update_product.html',{'form':form})

def del_product(request,id):
    Product.objects.get(id=id).delete()
    return redirect("viewproduct")

def service(request):
    return render(request,'services.html')

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('text')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_staff:
                auth.login(request, user)
                return redirect('admin')  
            elif user.is_customer:
                auth.login(request, user)
                return redirect('shop') 
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')

def signup(request):
    form1=customerreg()
    form2=userreg()
    if request.method=='POST':
            form2=customerreg(request.POST)
            form1=userreg(request.POST)
            if form1.is_valid() and form2.is_valid():
                user=form1.save(commit=False)
                user.is_customer=True
                user.save()
                cutomer=form2.save(commit=False)
                cutomer.user=user
                cutomer.save()
                return redirect('loginpage')

    return render(request,'signup.html',{'form1':form1,'form2':form2})

def admin(request):
    return render(request,'adminindex.html')

def logout_request(request):
    logout(request)
    messages.info(request,"Logged Out Successfully")
    return redirect("home")

def pro(request,id):
    data=Product.objects.get(id=id)
    return render(request, 'product_detail.html', {'data': data})

def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product,user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

def remove_from_cart(request, product_id):
    cart_item = CartItem.objects.get(id=product_id)
    cart_item.delete()
    return redirect('view_cart')

#def checkout(request):
    # Your checkout logic here
 #   return render(request, 'checkout.html')

def checkout(request):
    return render(request,'home.html')

def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
    
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'T-shirt',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': '2000',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
        
def payment(request):
    if request.method=='POST':
        amount=3000
        print(amount)
        description="Sample Payment"
        try:
           payment_intent=stripe.PaymentIntent.create(
               amount=amount,
               currency='inr',
               description=description,
           )
           Pay.objects.create(amount=amount/100,description=description)
        except Exception as e:
          return redirect('payment_success')
        return render(request,'payment_success.html',{'client_secret': payment_intent.client_secret})
    return render(request,'payment.html') 

def payment_success(request):
    return render(request,'payment_success.html')

def payment_status(request):
    customer_payments=Pay.objects.filter()
    return render(request,'payment_status.html',{'customer_payments':customer_payments})

def processs_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        card_number = request.POST.get('card_number')
        card_expiry = request.POST.get('card_expiry')
        card_cvv = request.POST.get('card_cvv')
        # Simulate payment processing
        # You can add actual payment processing logic here
        Payment.objects.create(amount=amount, card_number=card_number, card_expiry=card_expiry, card_cvv=card_cvv)
        return redirect('payment_successful') 
    return render(request, 'payment_form.html')

def payment_successful(request):
    return render(request, 'payment_successful.html')

def payment_statuss(request):
    # Retrieve payment status for the current user
    user_payment_status = Paystatus.objects.filter(user=request.user)
    
    
    context = {
        'user_payment_status': user_payment_status
    }
    return render(request, 'payment_statuss.html', context)

def process_payment(request):
         form=PaymentForm()
         u=request.user
         print(u)
         if request.method == 'POST':
             form = PaymentForm(request.POST)
             if form.is_valid():
                 obj = form.save(commit=False)
                 obj.user=u
                 obj.save()
                 return redirect('payment_success')
         return render(request, 'add_payment.html', {'form': form})


def view_payment(request):
    # Assuming customers are associated with users
    user_pay = Paymentz.objects.all()
    return render(request, 'payment_status.html', {'user_pay': user_pay})

def Review_rate(request,product_id):
    data = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review = form.save(commit=False)
            Review.product_id = product_id  # Assign product_id to review
            Review.save()
            return redirect('review_success')  # Redirect to a success page
    else:
        form = ReviewForm()
    return render(request, 'reviewpage.html', {'form': form})

def review_success(request):
    return render(request, 'review_success.html')

def view_reviews(request):
    data = Review.objects.all()
    return render(request, 'view_review.html', {'data': data})

def view_booking(request):
    user_pay=Paymentz.objects.all()
    return render(request,'booking.html', {'user_pay': user_pay})

def stock(request):
    products = productss.objects.all()
    return render(request, 'stock.html', {'products': products})



