from django.urls import path
from .views import CategoryView, ProductView, CartView, CartItemDeleteView, BuyView, ProfileView, MainView
urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('buy/', BuyView.as_view(), name='buy'),
    path('clear/', CartView.as_view(), name='clear_cart'),
    path('delete/', CartItemDeleteView.as_view(), name='delete'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add/', CartView.as_view(), name='add'),

    path('cat/<str:slug>/<str:product>/', ProductView.as_view(), name='cat_slug_product'),
    path('cat/<str:slug>/', CategoryView.as_view(), name='cat_slug'),
]