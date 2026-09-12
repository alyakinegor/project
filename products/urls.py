from django.urls import path
from .views import CategoryView, ProductView, CartView, CartItemDeleteView, BuyView, ProfileView
urlpatterns = [
    path('profile/', ProfileView.as_view()),

    path('buy/', BuyView.as_view()),
    path('clear/', CartView.as_view()),
    path('delete/', CartItemDeleteView.as_view()),
    path('cart/', CartView.as_view()),
    path('add/', CartView.as_view()),

    path('<str:slug>/<str:product>/', ProductView.as_view()),
    path('<str:slug>/', CategoryView.as_view()),
]