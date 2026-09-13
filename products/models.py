from django.db import models
from django.conf import settings
class Category(models.Model):
    cat_name = models.CharField(max_length=20, verbose_name='Название категории')
    slug = models.CharField(max_length=15, unique=True, verbose_name='URl-метка')

    def __str__(self):
        return self.cat_name

    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='products')
    title=models.CharField(max_length=100, verbose_name='Название')
    price=models.IntegerField(verbose_name='Цена')
    image = models.ImageField(upload_to='', verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    
    def __str__(self):
        return self.title

class Cart(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, 
        blank=True, related_name='cart')
    session_key = models.CharField(max_length=40, null=True, blank=True)

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.product.price * self.quantity

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
