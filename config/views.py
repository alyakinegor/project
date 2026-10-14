from django.shortcuts import render, redirect
from django.views import View
from .forms import RegistrationForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        return render(request, 'register.html', {'form': form})

@method_decorator(never_cache, name='dispatch')
class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

        
            return redirect('/')
        return render(request, 'login.html', {'form': form})

