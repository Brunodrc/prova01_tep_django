from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.http import HttpResponse
from my_wallet.models import Investor
from django.contrib import messages
from django.contrib.messages import constants
from django.urls import reverse

def landing_page(request):
    return render(request, 'accounts/landingpage.html')

def user_signup(request):
    risk_profile = Investor.RISK_PROFILE_CHOICES
    context = {
        'risk_profile': risk_profile
    }
    
    return render(request, 'accounts/signup.html', context=context)

def user_register(request):

    if request.method == 'GET':
        return redirect('user_signup')
    elif request.method == 'POST':
        # recede os dados do frontend
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        risk_profile = request.POST.get('risk_profile')
        
        if User.objects.filter(username=username).exists():
            messages.add_message(request, constants.ERROR, 'Usuário já cadastrado com esse nome')
            return redirect(reverse('user_signup'))
        
        if password1 != password2:
           
            messages.add_message(request, constants.ERROR, 'As senhas digitadas são diferentes.')
            return redirect(reverse('user_signup'))
    
        user = User.objects.create_user(username=username, password=password1)
        investor = Investor(user=user, risk_profile= risk_profile)
        investor.save()
        messages.add_message(request, constants.SUCCESS, "Pronto, seu cadastro foi salvo!")
        
        return redirect('user_signin')

def user_signin(request):
    return render(request, 'accounts/signin.html')

def user_login(request):
    if request.method == 'GET':
        return render(request, 'accounts/signin.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
    
    if user == None:
        messages.add_message(request, constants.ERROR, "Usuário ou senha incorretos.")
        return redirect(reverse('user_signin'))
    else:
        login(request, user)
    
        messages.add_message(request, constants.SUCCESS, "Logado com Sucesso!")
        return redirect('home')
    
def user_logout(request):
    logout(request)
    messages.add_message(request, constants.ERROR, "Usuário saiu do sistema!")
    return redirect('landing_page')