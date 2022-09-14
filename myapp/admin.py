from django.contrib import admin
from .models import User, Contact, Product_clothes,Wishlist,Cart, Address, Transaction
# Register your models here.
admin.site.register(User)
admin.site.register(Contact)
admin.site.register(Product_clothes)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(Transaction)
