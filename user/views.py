"""
views
"""

from django.core.mail import send_mail
from django.http import HttpResponse, FileResponse
from user.models import User, Image, Hero, Counter
from user.verify_code_gen import new_code, verify


def register(request):
    """
    register
    :param request: name, password, email, headImage
    :return: whether register succeeds
    """
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        try:
            if User.objects.get(name=name):
                return HttpResponse('username already exists')
        except User.DoesNotExist:
            pass
        try:
            if User.objects.get(email=email):
                return HttpResponse('email already exists')
        except User.DoesNotExist:
            pass
        code = str(new_code(email))
        try:
            if send_mail('registration', code, 'imtoosouth2019@163.com',
                         [email], fail_silently=False):
                return HttpResponse('send email success')
            return HttpResponse('send email failure')
        except NotImplementedError:
            return HttpResponse('send email failure')
    return HttpResponse('not POST request')


def login(request):
    """
    login
    :param request: name, password
    :return: whether login succeeds
    """
    if request.POST:
        try:
            user = User.objects.get(name=request.POST['name'],
                                    password=request.POST['password'])
        except User.DoesNotExist:
            return HttpResponse('login failure')
        if not user:
            return HttpResponse('login failure')
        return HttpResponse('login success')
    return HttpResponse('not POST request')


def send_code(request):
    """
    verify
    """
    if request.POST:
        name = request.POST['name']
        password = request.POST['password']
        email = request.POST['email']
        code = request.POST['code']
        if verify(email, code):
            User.objects.create(name=name,
                                password=password,
                                email=email)
            Counter.objects.create(name=name, num=0)
            return HttpResponse('register success')
        return HttpResponse('register failure')
    return HttpResponse('not POST request')


def upload_image(request):
    """
    upload headImage
    """
    if request.POST:
        name = request.POST['name']
        try:
            if Image.objects.get(name=name):
                Image.objects.get(name=name).delete()
        except Image.DoesNotExist:
            pass
        new_image = Image(name=name, headImage=request.FILES['image'])
        new_image.save()
        return HttpResponse('upload image success')
    return HttpResponse('not post request')


def download_image(request):
    """
    download headImage
    """
    if request.POST:
        name = request.POST['name']
        try:
            image = Image.objects.get(name=name).headImage.open(mode='rb')
        except Image.DoesNotExist:
            return FileResponse(open('default.png', mode='rb'))
        return FileResponse(image)
    return HttpResponse('not post request')


def upload_hero(request):
    """
    upload hero
    """
    if request.POST:
        name = request.POST['name']
        num = Counter.objects.get(name=name).num
        new_hero = Hero(name=name, heroImage=request.FILES['image'], index=num)
        new_hero.save()
        Counter.objects.get(name=name).delete()
        Counter.objects.create(name=name, num=num+1)
        return HttpResponse('upload hero success')
    return HttpResponse('not post request')


def download_hero_image(request):
    """
    download hero image
    """
    if request.POST:
        name = request.POST['name']
        index = request.POST['index']
        try:
            hero = Hero.objects.get(name=name, index=index)
        except Hero.DoesNotExist:
            return HttpResponse('Hero does not exist')
        image = hero.heroImage.open(mode='rb')
        response = FileResponse(image)
        response['Content-Disposition'] = hero.heroImage.name
        return response
    return HttpResponse('not post request')


def download_hero_names(request):
    """
    download hero num
    """
    if request.POST:
        name = request.POST['name']
        num = Counter.objects.get(name=name).num
        text = ""
        for i in range(num):
            hero = Hero.objects.get(name=name, index=i)
            text += hero.heroImage.name[11:] + '\n'
        return HttpResponse(text)
    return HttpResponse('not post request')


def delete_hero(request):
    """
    delete hero
    """
    if request.POST:
        name = request.POST['name']
        index = request.POST['index']
        Hero.objects.get(name=name, index=index).delete()
        counter = Counter.objects.get(name=name)
        for i in range(int(index) + 1, counter.num):
            hero = Hero.objects.get(name=name, index=i)
            hero.index -= 1
            hero.save()
        counter.num -= 1
        counter.save()
        return HttpResponse('delete hero success')
    return HttpResponse('not post request')


def change_password(request):
    if request.POST:
        name = request.POST['name']
        old_password = request.POST['old']
        new_password = request.POST['new']
        user = User.objects.get(name=name)
        if old_password != user.password:
            return HttpResponse('password incorrect')
        user.password = new_password
        user.save()
        return HttpResponse('password changed')
    return HttpResponse('not post request')


def find_password(request):
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        try:
            user = User.objects.get(name=name)
            if user.email != email:
                return HttpResponse('user and email does not match')
        except User.DoesNotExist:
            return HttpResponse('user does not exist')
        code = str(new_code(email))
        try:
            if send_mail('change password', code, 'imtoosouth2019@163.com',
                         [email], fail_silently=False):
                return HttpResponse('send email success')
            return HttpResponse('send email failure')
        except NotImplementedError:
            return HttpResponse('send email failure')
    return HttpResponse('not post request')


def verify_find_password(request):
    if request.POST:
        name = request.POST['name']
        password = request.POST['password']
        email = request.POST['email']
        code = request.POST['code']
        if verify(email, code):
            user = User.objects.get(name=name)
            user.password = password
            user.save()
            return HttpResponse('change password success')
        return HttpResponse('change password failure')
    return HttpResponse('not POST request')
