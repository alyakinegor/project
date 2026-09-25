from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Class
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Lower, Replace
from django.contrib.auth.models import AnonymousUser
from django.db.models import Value, Sum
from django.db import transaction
import json
from django.contrib.auth import logout
from django.http import JsonResponse
# Create your views here.
class CategoryView(View):
    def get(self, request, slug):

        category = get_object_or_404(Category, slug=slug)

        products = Product.objects.filter(category=category)
        return render(request, 'catalog.html', {'category': category,
                                             'products': products})

class ProductView(View):
    def get(self,  request,slug, product):
        queryset = Product.objects.annotate(formatted_data=Lower(Replace(Replace(Replace(Replace('title', Value(' '), Value('-')), Value('"'), Value('')), Value('.'), Value('')), Value('/'), Value(''))))
        item = get_object_or_404(queryset, formatted_data=product)
        classes = Class.objects.all()
        return render(request, 'product_detail.html', {'product': item, 'classes': classes})

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart

class CartView(View):
    def post(self, request):
            try:
                data = json.loads(request.body)
                pr_id = data.get('product_id')
                cart = get_or_create_cart(request)
                product = Product.objects.get(id=pr_id)

                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                if not created:
                    cart_item.quantity += 1
                    cart_item.save()
                
                cart_item.product.quantity_left -= 1
                cart_item.product.save()
                
                
                return JsonResponse({'status': 'ok', 'message': 'Товар добавлен'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    def get(self, request):
        cart = get_or_create_cart(request)
        cart_items = CartItem.objects.filter(cart=cart).select_related('product')
        return render(request, 'cart.html', {'items': cart_items, 'total_price': cart.get_total_price()})

    def delete(self, request):
            cart = get_or_create_cart(request)
            CartItem.objects.filter(cart=cart).delete()
            return JsonResponse({'status': 'ok'})

class CartItemDeleteView(View):
    def get(self, request):
        return redirect('/cart/')
    
    def post(self, request):
        cart = get_or_create_cart(request)
        data = json.loads(request.body)
        pr_id = data.get('product_id')
        try:
            item = CartItem.objects.get(product=Product.objects.get(id=pr_id), cart=cart)
            item.product.quantity_left += item.quantity
            item.product.save()
            item.delete()
        except Exception:
            return JsonResponse({'error': 'Ошибка при удалении товара'}, status=500)
        return JsonResponse({'status': 'ok'})



class BuyView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request):
        cart = get_or_create_cart(request)
        cart_items = cart.items.select_related('product').all()

        if len(cart_items) > 0:
            with transaction.atomic():
                if request.POST.get('address'):
                    order = Order.objects.create(user = request.user if request.user.is_authenticated else None, address=request.POST.get('address'), summary=cart.get_total_price())
                else:
                    return render(request, 'cart.html', {'items': cart_items, 'total_price': cart.get_total_price(), 'error': 'Обязательное поле.'})

                order_items_to_create = [
                    OrderItem(order=order,
                            product=item.product,
                            quantity=item.quantity,
                            price=item.product.price) for item in cart_items
                ]

                OrderItem.objects.bulk_create(order_items_to_create)

                CartItem.objects.filter(cart=cart).delete()

            return redirect('/profile/')
        return redirect('/')

class ProfileView(View):
    def get(self, request):
        if not isinstance(request.user, AnonymousUser):
                
            orders = Order.objects.filter(user=request.user)
            return render(request, 'profile.html', {'orders': orders})
        else:
             return render(request, 'profile.html')
    def post(self, request):
        logout(request)

        return redirect('/')

class MainView(View):
    def get(self, request):
        try:
            t1 = Product.objects.get(id=1)
            t2 = Product.objects.get(id=4)
            t3 = Product.objects.get(id=5)

            return render(request, 'main.html', {'specials': [t1, t2, t3]})
        except Exception:
            return render(request, 'main.html')