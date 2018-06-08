from django.urls import path

from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_id>/', views.detail, name='detail'),
    path('register', views.register, name='register'),
    path('login', views.custom_login, name='login'),
    path('logout', auth_views.logout, {'next_page': '/'}, name='logout'),
]
