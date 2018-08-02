from django import forms


class LoginForm(forms.Form):
    # required默认为Ture
    username = forms.CharField(error_messages={'required': '用户名不能为空！'})
    password = forms.CharField(
        min_length=8,
        error_messages={
            'required': '密码不能为空！',
            'min_length': '密码长度至少是8位！',
        })

class RegisterForm(forms.Form):
    email = forms.CharField(error_messages={'required': '用户名或邮箱不能为空！'})
    pwdInitial = forms.CharField(error_messages={'required': '请输入密码！', 'min_length': '密码长度至少是8位'})
    pwdRepeat = forms.CharField(error_messages={'required': '请再次输入密码！'})