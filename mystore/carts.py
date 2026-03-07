from .models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        
        # If product already exists, update quantity, otherwise add new
        if product_id in self.cart:
            self.cart[product_id]['qty'] = int(quantity)
        else:
            self.cart[product_id] = {
                'price': str(product.price),
                'qty': int(quantity)
            }
            
        self.session.modified = True

    def __len__(self):
        # This allows you to use {{ cart|length }} in templates
        return len(self.cart)

    def get_prods(self):
        # 1. Get IDs from cart
        product_ids = self.cart.keys()
        # 2. Look up products in database
        products = Product.objects.filter(id__in=product_ids)
        return products

    def delete(self, product):
        product_id = str(product)
        # Check if the product is in our cart dictionary
        if product_id in self.cart:
            del self.cart[product_id]
        
        # Critical: Tell Django the session changed so it saves the deletion
        self.session.modified = True

    def get_total_price(self):
        # 1. Get all product IDs currently in the cart session
        product_ids = self.cart.keys()
        
        # 2. Look up those products in the database
        products = Product.objects.filter(id__in=product_ids)
        
        total = 0
        for product in products:
            # 3. Get the item data from session to find the quantity
            item = self.cart[str(product.id)]
            
            # 4. Multiply price by quantity (default to 1 if qty is missing)
            quantity = int(item.get('qty', 1))
            total += float(product.price) * quantity
            
        return total

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # Update the quantity in our session dictionary
        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_qty

        self.session.modified = True    
