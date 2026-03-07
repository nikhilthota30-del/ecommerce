from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('login', views.login_user, name='login'), 
    path('add/', views.cart_add, name='cart_add'),
    path('cart/', views.cart_summary, name='cart_summary'),
    path('delete/', views.cart_delete, name='cart_delete'),
    path('update/', views.cart_update, name='cart_update'),
    path('logout/', views.logout_user, name='logout'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('profile/', views.profile, name='profile'),
    path('orders/', views.orders, name='orders'),
    path('checkout/', views.checkout, name='checkout'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('search/', views.search, name='search'),
    path('live-search/', views.live_search, name='live_search'),
    path('cart-clear/', views.cart_clear, name='cart_clear'),
]