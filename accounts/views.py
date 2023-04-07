from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import SignupForm


def home(request):
    return redirect('/login')

def signup(request):
    if request.method == "POST": #POST 방식으로 접근
        form = SignupForm(request.POST) # SignupForm 모델을 이용하여 회원가입 진행
        if form.is_valid(): #유효성 검사 실행
            form.save()  #통과하면 저장, 이하 회원가입 후 로그인
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')

            user = authenticate(username=username, password=password, email=email) #유효성  검사
            login(request, user)
            return redirect('signup')
    else:
        form = SignupForm() #GET방식으로 들어왔을 때 회원가입 폼을 출력
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('manage/product_list.html')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
