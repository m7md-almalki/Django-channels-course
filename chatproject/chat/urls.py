from django.urls import path
from . import views


urlpatterns = [
    path('', views.Main.as_view(), name="main"),
    path('login', views.Login.as_view(), name="login"),
    path('register', views.Register.as_view(), name="register"),
    path('logout', views.Logout.as_view(), name="logout"),
    path('home', views.Home.as_view(), name="home"),
    path('chat_person/<int:id>', views.ChatPerson.as_view(), name="chat_person"),
]
