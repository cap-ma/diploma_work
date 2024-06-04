from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name=models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.name
    

class Product(models.Model):
    name=models.CharField(max_length=250,verbose_name='nomi')
    image=models.ImageField(upload_to='media/')
    price=models.DecimalField(max_digits=15,decimal_places=2,verbose_name='narxi')
    description=models.TextField(verbose_name='mahsulot haqida')
    in_stock=models.BooleanField(default=True)
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,blank=True,null=True)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)


    def __str__(self) -> str:
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.created_at)

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products',null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=15, decimal_places=2,default=0,null=True,blank=True)

    def __str__(self) -> str:
        return self.product.name


