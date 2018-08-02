import random
import string
import redis
from django.core.mail import send_mail
from shopping_project.settings import DEFAULT_FROM_EMAIL, HOST_URL


def random_letters(length=16):
    letters = string.ascii_letters + string.digits
    ret = ''.join(random.sample(letters, length))
    return ret


# 发送邮件
def send_emails(email, send_type='register'):
    '''
    db: 1是注册，2是忘记密码，3是更改密码
    :param email:接收的邮箱地址
    :param send_type: 注册（register）, 忘记密码(forget),更改密码(update)
    :return:
    '''
    msg = '验证码两分钟内有效，已发送至您的邮箱,请注意查收！'
    # msg = '验证码已发送至您的邮箱，请不要在两分钟内重复申请！'
    flag = True
    if send_type == 'register':
        r1 = redis.Redis(db=1, decode_responses=True)
        if r1.get(email):
            msg = '验证码已发送至您的邮箱，请不要在两分钟内重复申请！'
            flag = False
        else:
            code = random_letters()
            r1.set(email, code, ex=120)
            email_title = "在线商城注册激活链接"
            email_body = "请点击下面的链接激活你的账户：{1}active/{2}/{0}".format(code, HOST_URL, email)
            flag = send_mail(email_title, email_body, DEFAULT_FROM_EMAIL, [email])
    elif send_type == 'forget':
        r2 = redis.Redis(db=2, decode_responses=True)
        if r2.get(email):
            msg = '验证码已发送至您的邮箱，请不要在两分钟内重复申请！'
            flag = False
        else:
            code = random_letters()
            r2.set(email, code, ex=120)
            email_title = "在线商城重置密码链接"
            email_body = "请点击下面的链接重置你的密码：{1}reset/{0}".format(code, HOST_URL)
            flag = send_mail(email_title, email_body, DEFAULT_FROM_EMAIL, [email])
    elif send_type == 'update':
        r3 = redis.Redis(db=3, decode_responses=True)
        if r3.get(email):
            msg = '验证码已发送至您的邮箱，请不要在两分钟内重复申请！'
            flag = False
        else:
            code = random_letters(4)
            r3.set(email, code, ex=120)
            email_title = "在线商城邮箱修改验证码"
            email_body = "你的邮箱验证码为: {0}".format(code)
            flag = send_mail(email_title, email_body, DEFAULT_FROM_EMAIL, [email])
    return flag, msg


def check_code(db, email, code):
    '''
    :param:db: 1是注册，2是忘记密码，3是更改密码
    :param email: 用户的注册邮箱地址
    :param code: 验证码
    :return:若验证通过返回True,否则False
    '''
    rx = redis.Redis(db=db, decode_responses=True)
    if rx.get(email) == code:
        return True
    return False


if __name__ == '__main__':
    r1 = redis.Redis(db=1, decode_responses=True)
    # r1.set('s1', 'hello world', ex=5)
    # 不用get方式会出错。
    # print(r1['s1'])
    # r1.shutdown()
    print(r1.get('s1'))
    print(type(r1.get('s1')))
