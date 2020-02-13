"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from user.views import register, login, send_code, upload_hero, \
    upload_image, download_hero_image, download_image, download_hero_names, \
    delete_hero, change_password, verify_find_password, find_password
from room.views import creat_room, get_all_room, get_single_room, verify, \
    quick_start, get_all_player

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('sendCode/', send_code),
    path('upload/image/', upload_image),
    path('upload/hero/', upload_hero),
    path('download/image/', download_image),
    path('download/hero/image/', download_hero_image),
    path('download/hero/names/', download_hero_names),
    path('delete/hero/', delete_hero),
    path('room/create/', creat_room),
    path('room/getAll/', get_all_room),
    path('room/getSingle/', get_single_room),
    path('changePassword/', change_password),
    path('findPassword/', find_password),
    path('sendResetCode/', verify_find_password),
    path('room/verify/', verify),
    path('room/quickStart/', quick_start),
    path('room/getAllPlayer/', get_all_player),
]
