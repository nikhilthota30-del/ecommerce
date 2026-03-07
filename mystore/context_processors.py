from .carts import Cart

# mystore/context_processors.py

def cart(request):
    return {'cart': request.session.get('cart', {})}

def cart_count(request):
    cart_data = request.session.get('cart', {})
    count = 0
    
    if isinstance(cart_data, dict):
        for item in cart_data.values():
            # If your cart stores items as dictionaries: {'price': 99, 'qty': 1}
            if isinstance(item, dict):
                count += int(item.get('qty', 0))
            # If your cart stores items as simple integers: {id: quantity}
            else:
                count += int(item)
                
    return {'cart_count': count}