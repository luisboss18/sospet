from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Pet


@login_required(login_url='/login/')
def register_pet(request):
    pet_id = request.GET.get('id')
    if pet_id:
        pet = Pet.objects.get(id=pet_id)
        print(pet.city)
        return render(request, 'register-pet.html', {'pet':pet})
    return render(request,'register-pet.html')


@login_required(login_url='/login/')
def set_pet(request):
    city = request.POST.get('city')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    description = request.POST.get('description')
    file = request.FILES.get('file')
    user = request.user
    pet = Pet.objects.create(email=email, phone=phone, description=description, 
                             photo=file, city=city, user=user)
    url = '/pet/detail/{}/'.format(pet.id)                                                     
    return redirect(url)

@login_required(login_url='/login/')
def delete_pet(request, id):
    pet = Pet.objects.get(id=id)
    if pet.user == request.user:
        pet.delete()
    return redirect('/')

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