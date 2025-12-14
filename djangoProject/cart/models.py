from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

from django.utils.html import MAX_URL_LENGTH


#Product and Cart Models
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField(blank=True)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())
    
    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def get_subtotal(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

#Order Model
#Creating Order class. (one user can own a multiple orders)
class Order(models.Model):
    #order status  1 -- create the status
    STATUS_CHOICES = [
        ('pending' , 'Pending Payment'),
        ('delivered', 'Delivered'),
        ('shipping', 'Shiping'),
        ('cancelled', 'Cancelled'),
        ('processing' , 'Processing'),
    ]
    
    #an a object just can be linked to one other object. OnetoOne
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length = 50, unique = True)
    #like an a form option, the choices has the value of status.
    status = models.CharField(max_length = 20, choices = STATUS_CHOICES, default = 'pending')

    #creating the total amount of order, discount and final value
    total_amount = models.DecimalField(max_digits = 10,decimal_places = 2)
    discount = models.DecimalField(max_digits = 10, decimal_places = 2)
    final_amount = models.DecimalField(max_digits = 10, decimal_places = 2)

    #creating the payment method and id of the order
    payment_method = models.CharField(max_length = 15, blank = True)
    payment_id = models.CharField(max_length = 15, blank = True, null = True)

    #tracking code attached to the order, correios.
    tracking_code = models.CharField(max_length = 14 ,blank = True, default = 'not posted yet')

    #shipping infos
    shipping_adress = models.TextField()
    shipping_city = models.CharField(max_length = 100 , blank = True, null = True)
    shipping_state = models.CharField(max_length = 2, blank = True,null = True)
    shipping_zipcode = models.CharField(max_length = 20)

    #date and time
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    #setting how the object gonn be called.
    def __str__(self):
        return f"Order : {self.order_number} - {self.user.username}"

    def get_status_badge_class(self):
        if self.status == 'pending':
            return 'bg-warning'
        elif self.status == 'processing':
            return 'bg-info'
        elif self.status == 'shipping':
            return 'bg-primary'
        elif self.status == 'delivered':
            return 'bg-success'
        elif self.status == 'cancelled':
            return 'bg-danger'
        else:
            return 'bg-secondary'

    #order the orders to the most recent 
    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name = "items" , on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length = 2,blank = True, null = True)
    price = models.DecimalField(max_digits = 10 , decimal_places = 2)

    def get_subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} X {self.product.name}"

