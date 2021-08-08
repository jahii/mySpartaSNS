from django.shortcuts import render,redirect
from .models import Usermodel
from django.http import HttpResponse
from django.contrib.auth import get_user_model #사용자가 데이터베이스 안에 있는지 검사하는 함수
from django.contrib import auth
from django.contrib.auth.decorators import login_required


# Create your views here.
def sign_up_view(request): #회원가입
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else :            
            return render(request, 'user/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')
        #기존에 사용자가 있으면 check 변수안에 불러들임
        check = get_user_model().objects.filter(username = username)

        if password != password2 :
            #패스워드가 같지 않다고 알람

            return render(request,'user/signup.html',{'error':'패스워드를 확인해 주세요!'})
        elif username == '' or password =='':
            return render(request, 'user/signup.html', {'error' : '사용자 이름과 비밀번호는 필수 값입니다!'})
        elif check:
            return render(request, 'user/signup.html', {'error':'사용자가 존재합니다'})

        else:
            Usermodel.objects.create_user(username=username, password = password, bio = bio)
        return redirect('/sign-in')

def sign_in_view(request): #login
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, username =username, password = password)
        
        if me is not None:
            auth.login(request, me)
            return redirect('/')
        else:
            return render(request, 'user/signin.html', {'error':'유저 이름 혹은 패스워드를 확인해 주세요'})

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')
# user/views.py 

@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = Usermodel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user
    click_user = Usermodel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')