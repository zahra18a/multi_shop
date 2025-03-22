from django.db import models
from account.models import User
from product.models import Product


class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    total_price=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    is_paid=models.BooleanField(default=False)


class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE, related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE, related_name='items')
    size=models.CharField(max_length=10)
    color=models.CharField(max_length=10)
    price=models.PositiveIntegerField()
    quantity=models.SmallIntegerField()


