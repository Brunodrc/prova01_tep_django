from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.http import HttpResponse
from my_wallet.models import Investor

def landing_page(request):
    return render(request, 'accounts/landingpage.html')

def user_signup(request):
    risk_profile = Investor.RISK_PROFILE_CHOICES
    context = {
        'risk_profile': risk_profile
    }
    
    return render(request, 'accounts/signup.html', context=context)

def user_register(request):
    # recede os dados do frontend
    username = request.POST.get('username')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    risk_profile = request.POST.get('risk_profile')

    # usar mensagens do django

    if User.objects.filter(username=username).exists():
        error_msg = 'Usuário já cadastrado com esse nome'
        return HttpResponse(error_msg)
    if password1 != password2:
        error_msg2 = 'As senhas digitadas são diferentes.'
        return HttpResponse(error_msg2)
    
    user = User.objects.create_user(username=username, password=password1)
    investor = Investor(user=user, risk_profile= risk_profile)
    investor.save()
    info = 'Cadastro realizado com sucesso!'
    print(f'{user}-- {investor}')
    return redirect('user_signin')

def user_signin(request):
    return render(request, 'accounts/signin.html')

def user_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    
    if user == None:
        return HttpResponse('usuário ou senha inválidos.')
    else:
        login(request, user)
    # TODO: acrescentar mensagens django
        print('usuário logado com sucesso!')
        return redirect('home')
def user_logout(request):
    logout(request)
    return redirect('landing_page')