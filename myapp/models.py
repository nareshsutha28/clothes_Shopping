from django.db import models
from django.utils import timezone

# Create your models here.
CHOICE=(
        ('user', 'user'),
        ('seller', 'seller'),
    )
    
class User(models.Model):
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    mobile=models.PositiveIntegerField()
    city=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    profile=models.ImageField(upload_to='profile/')
    usertype=models.CharField(max_length=100, choices=CHOICE)

    def __str__(self):
        return self.fname+" "+self.lname


class Contact(models.Model):
    fname=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    subject=models.CharField(max_length=100)
    message=models.TextField()
    image=models.ImageField(upload_to= 'media/contact/')

    def __str__(self):
        return self.email

category=(
    ('woman_wear','woman_wear' ),
    ('man_wear', 'man_wear'),
    ('kid_wear', 'kid_wear')
)

class Product_clothes(models.Model):
    seller=models.ForeignKey('User', on_delete=models.CASCADE)
    product_category=models.CharField(max_length=100, choices=category)
    product_name=models.CharField(max_length=100)
    product_prise=models.PositiveIntegerField()
    product_cprise=models.PositiveIntegerField()

    product_discount=models.PositiveIntegerField()
    product_size=models.CharField(max_length=100)
    product_color=models.CharField(max_length=100)
    product_disc=models.TextField()
    product_image=models.ImageField(upload_to='product/')

    def __str__(self):
        return self.seller.fname+ " "+self.product_category



class Wishlist(models.Model):
    seller=models.ForeignKey('User', on_delete=models.CASCADE)
    product=models.ForeignKey('Product_clothes', on_delete=models.CASCADE)
    time=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.seller.fname+ " "+self.product.product_name

class Cart(models.Model):
    user=models.ForeignKey('User', on_delete=models.CASCADE)
    product=models.ForeignKey('Product_clothes', on_delete=models.CASCADE)
    time=models.DateTimeField(default=timezone.now)
    product_qty=models.PositiveIntegerField(default=1)
    total_prise=models.PositiveIntegerField()
    payment_status=models.CharField(max_length=100, default='pending')

    def __str__(self):
        return self.user.fname+ " "+self.product.product_name

class Address(models.Model):
    user=models.ForeignKey('User', on_delete=models.CASCADE)
    address_1=models.CharField(max_length=100)
    address_2=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    zipcode=models.CharField(max_length=100)
    contry=models.CharField(max_length=100)

    def __str__(self):
        return self.user.fname+ " "+"Address"


class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
