import email
from urllib import request

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.db import transaction
from .models import Product, Category, Customer, Order
from .carts import Cart

# Create your views here.

def home(request):
    categories = Category.objects.all()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.objects.filter(category_id=categoryID)
    else:
        products = Product.objects.all()    
    data = {'products': products, 'categories': categories}
    return render(request, 'index.html', data)


def signup(request):
    if request.method == 'POST':
        # Change this line:
        em = request.POST.get('email')
        ps = request.POST.get('password')
        fn = request.POST.get('firstname')
        
        # Set 'un' to be the email address
        un = em 

        if not un:
            messages.error(request, "Email is required.")
            return render(request, 'signup.html')

        if User.objects.filter(username=un).exists():
            messages.error(request, "This email is already registered.")
            return render(request, 'signup.html')

        # Now 'un' is 'nikh@gmail.com' instead of None
        user = User.objects.create_user(username=un, email=em, password=ps, first_name=fn)
        
        messages.success(request, "Account created!")
        return redirect('login')


def login_user(request):
    if request.method == 'POST':
        # 1. Grab data using the EXACT 'name' from your HTML
        un = request.POST.get('username') 
        ps = request.POST.get('password')

        # 2. Authenticate against the User table
        # This works for 'admin' (from build command) or email (from signup)
        user = authenticate(request, username=un, password=ps)

        if user is not None:
            # 3. Create the session
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            # 4. If authentication fails
            messages.error(request, "Invalid username or password. Please try again.")
            return render(request, 'login.html')

    # If it's a GET request, just show the page
    return render(request, 'login.html')

def logout_user(request):
    request.session.flush() 
    return redirect('home')

def cart_delete(request):
    if request.POST.get('action') == 'post':
        product_id = str(request.POST.get('product_id'))
        cart = request.session.get('cart', {})

        if product_id in cart:
            del cart[product_id]
            
            # This is the "Save" button for the session
            request.session['cart'] = cart
            request.session.modified = True 

        # Return the count so the AJAX can update the badge immediately
        return JsonResponse({'qty': sum(int(item['qty']) for item in cart.values())})

    
def cart_update(request):
    if request.POST.get('action') == 'post':
        product_id = str(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart = request.session.get('cart', {})
        cart[product_id] = product_qty
        request.session['cart'] = cart
        request.session.modified = True
        total = 0
        for p_id, qty in cart.items():
            product = Product.objects.get(id=p_id)
            total += (product.price * qty)
        cart_count = sum(cart.values())
        return JsonResponse({'qty': cart_count, 'total': total})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def profile(request):
    # Search by email instead of the non-existent 'user' field
    customer = Customer.objects.get(email=request.user.email) 
    return render(request, 'profile.html', {'customer': customer})
    



def cancel_order(request, order_id):
    if request.method == "POST":
        customer_id = request.session.get('customer_id')
        if not customer_id:
            return redirect('login')
        order = get_object_or_404(Order, id=order_id, customer_id=customer_id)
        order.delete()
        messages.success(request, "Order has been cancelled successfully.")
    return redirect('orders')

def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query) if query else Product.objects.none()
    categories = Category.objects.all()
    data = {'products': products, 'categories': categories, 'query': query}
    return render(request, 'index.html', data)

def live_search(request):
    query = request.GET.get('q', '')
    data = []
    if len(query) > 1:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query)
        )[:5]
        for p in products:
            data.append({
                'name': p.name,
                'price': str(p.price),
                'url': f"/product/{p.id}/",
            })
    return JsonResponse({'data': data})

def cart_clear(request):
    # Set the cart session to an empty dictionary
    request.session['cart'] = {}
    request.session.modified = True
    
    messages.success(request, "Cart cleared successfully!")
    return redirect('cart_summary')




def cart_add(request):
    # We check for 'action' == 'post' because that's what your AJAX sends
    if request.POST.get('action') == 'post':
        # 1. Capture the ID from the AJAX data
        product_id = request.POST.get('product_id')
        
        # 2. Find the product
        product = get_object_or_404(Product, id=product_id)

        # 3. Get the existing cart or create an empty one
        cart = request.session.get('cart', {})

        # 4. Add the product (or increase quantity if it already exists)
        if str(product_id) in cart:
            cart[str(product_id)]['qty'] += 1
        else:
            cart[str(product_id)] = {
                'qty': 1,
                'price': str(product.price)
            }

        # 5. Save back to session
        request.session['cart'] = cart
        request.session.modified = True
        
        # 6. Calculate TOTAL number of items in the cart
        # This sums up all 'qty' values in your cart dictionary
        cart_count = sum(item['qty'] for item in cart.values())

        # 7. Return JSON instead of a redirect
        return JsonResponse({
            'qty': cart_count,
            'product_name': product.name
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)



def cart_summary(request):
    cart_session = request.session.get('cart', {})
    cart_items = []
    grand_total = 0
    
    for product_id, item_data in cart_session.items():
        product = get_object_or_404(Product, id=product_id)
        
        # Get quantity safely
        qty = int(item_data.get('qty', 1)) if isinstance(item_data, dict) else int(item_data)
        
        # We only need the grand total now
        grand_total += float(product.price) * qty
        
        cart_items.append({
            'product': product,
            'quantity': qty,
        })

    return render(request, 'cart_summary.html', {
        'cart_items': cart_items, 
        'grand_total': grand_total
    })

def checkout(request):
    # This will print in your VS Code terminal
    print(f"DEBUG: User is {request.user}")
    print(f"DEBUG: Is Auth? {request.user.is_authenticated}")

    if request.method == 'POST':
        # If this triggers, your session isn't holding the login
        if not request.user.is_authenticated:
            return HttpResponse("DEBUG ERROR: Server says you are NOT logged in.")

        cart = request.session.get('cart', {})
        
        # Ensure a Customer profile exists for this user
        # This prevents errors if the Customer table is empty
        customer, created = Customer.objects.get_or_create(
            email=request.user.email,
            defaults={'first_name': request.user.username}
        )

        address = request.POST.get('address', 'Default Address')
        phone = request.POST.get('phone', '0000000000')

        for p_id, qty in cart.items():
            product = get_object_or_404(Product, id=p_id)
            Order.objects.create(
                product=product,
                customer=customer,
                quantity=qty if isinstance(qty, int) else qty.get('qty', 1),
                price=product.price,
                address=address,
                phone=phone
            )

        request.session['cart'] = {}
        request.session.modified = True
        return redirect('orders')
    
    return HttpResponse("DEBUG ERROR: You didn't send a POST request.")


def orders(request):
    if not request.user.is_authenticated:
        return redirect('login')

    customer = Customer.objects.filter(email=request.user.email).first()

    if customer:
        # select_related fetches product info in one go, making it faster
        order_list = Order.objects.filter(customer=customer).select_related('product').order_by('-date')
        return render(request, 'orders.html', {'orders': order_list})

    messages.error(request, "No order history found.")
    return redirect('home')





def cart_count(request):
    cart = request.session.get('cart', {})
    # Sum up the quantities of all items in the session
    count = sum(item['qty'] for item in cart.values())
    return {'cart_count': count}