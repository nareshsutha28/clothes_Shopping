
from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('cart/', views.cart, name='cart'),
        # path('shop/', views.shop, name='shop'),
        path('checkout/', views.checkout, name='checkout'),
        path('contact/', views.contact, name='contact'),
        path('logout/', views.logout, name='logout'),
        path('login/', views.login, name='login'),
        path('signup/', views.signup, name='signup'),
        path('forgot_password/', views.forgot_password, name='forgot_password'),
        path('otp_verify/', views.otp_verify, name='otp_verify'),
        path('create_password/', views.create_password, name='create_password'),
        path('change_password/', views.change_password, name='change_password'),
        path('user_profile/', views.user_profile, name='user_profile'),
        path('seller_index/', views.seller_index, name='seller_index'),
        path('seller_add_product/', views.seller_add_product, name='seller_add_product'),
        path('seller_myproduct/', views.seller_myproduct, name='seller_myproduct'),
        path('seller_contact/', views.seller_contact, name='seller_contact'),
        path('seller_product_profile/<int:pk>/', views.seller_product_profile, name='seller_product_profile'),
        path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
        path('seller_edit_product/<int:pk>/', views.seller_edit_product, name='seller_edit_product'),
        path('view_product/<int:pk>/', views.view_product, name='view_product'),
        path('by_category/<str:pc>/', views.by_category, name='by_category'),
        path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
        path('add_to_wishlist/<int:pk>/', views.add_to_wishlist, name='add_to_wishlist'),
        path('wishlist/', views.wishlist, name='wishlist'),
        path('remove_from_wishlist/<int:pk>/', views.remove_from_wishlist, name='remove_from_wishlist'),
        path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
        path('remove_from_cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
        path('change_qty/<int:pk>/', views.change_qty, name='change_qty'),
        path('add_address/', views.add_address, name='add_address'),
        path('remove_address/<int:apk>', views.remove_address, name='remove_address'),
        path('pay/', views.pay, name='pay'),
        path('callback/', views.callback, name='callback'),
        path('myorder/', views.myorder, name='myorder'),
        path('seller_by_category/<str:pc>', views.seller_by_category, name='seller_by_category'),








        # 'user_profile'
]
