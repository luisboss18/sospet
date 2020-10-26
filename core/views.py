from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Pet


def register_pet(request):
    return render(request,'register-pet.html')

@login_required(login_url='/login/')
def list_all_pets(request):
    pet = Pet.objects.filter(active=True)
    return render(request, 'list.html', {'pet':pet}) 

def list_user_pets(request):
    pet = Pet.objects.filter(active=True, user=request.user)
    return render(request,'list.html', {'pet':pet})  

def pet_detail(request, id):
    pet = Pet.objects.get(active=True, id=id)
    print(pet.id)
    return render(request,'pet.html', {'pet':pet})

def logout_user(request):
    logout(request)
    return redirect('/login/')

def login_user(request):
    return render (request, 'login.html')

@csrf_protect
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Usuário e senha inválidos. Favor tentar novamente.')
    return redirect('/login/') 