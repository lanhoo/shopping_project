from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views.generic.base import View
from django.contrib.auth import authenticate, logout, login
from Shopping.forms import LoginForm, RegisterForm
from Shopping.models import UserProfile
from django.contrib.auth.hashers import make_password
from Shopping.utils.send_email import send_emails, check_code


def index(request):
    return render(request, 'index.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # print(request.POST)

        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')

            user = authenticate(username=username, password=password)
            if user:
                if user.user_status:
                    login(request, user)
                    return redirect('index')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活！请到您所注册的邮箱中进行激活操作。'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误！'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            pwd1 = request.POST.get('pwdInitial', '')
            pwd2 = request.POST.get('pwdRepeat', '')

            if UserProfile.objects.filter(email=email).filter(user_status=True):
                return render(request, 'register.html', {'msg': '此邮箱已经注册了！'})
            elif UserProfile.objects.filter(email=email).filter(user_status=False):
                flag, msg = send_emails(email, 'register')
                if flag:
                    return render(request, 'register.html',
                                  {'msg': '验证码已重新发送至您的邮箱，两分钟内有效。密码是您第一次注册所填写，若忘记密码，请至首页点击忘记密码。'})
                else:
                    return render(request, 'register.html', {'msg': msg})
            if pwd1 != pwd2:
                return render(request, 'register.html', {'msg': '两个密码不一致！'})
            user = UserProfile()
            user.email = email
            user.username = email
            user.password = make_password(pwd1)
            user.user_status = False

            user.save()
            # 注册完后发送验证邮件
            flag, msg = send_emails(email, 'register')
            print(msg)

        return render(request, 'register.html', {'reg_form': register_form})


class UserActiveView(View):
    def get(self, request, email, active_code):

        if check_code(db=1, email=email, code=active_code):
            user = UserProfile.objects.filter(email=email).first()
            user.user_status = True
            user.save()
            return redirect('login')
        return HttpResponse('您的验证码已过期，请重新注册。密码是您最初注册时的密码，若忘记密码请在主页上点击忘记密码。')


class Logout(View):
    def get(self, reqeust):
        logout(reqeust)
        return redirect('index')


class Forget(View):
    def get(self, reqeust):
        return HttpResponse('forget')
