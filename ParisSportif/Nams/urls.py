"""ParisSportif URL Configuration

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
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.redir),
    path('home',views.home, name="home"),
    path('nam\'ser/register',views.Register,name="register"),
    path('nam\'ser/login',views.Login,name="login"),
    path('logout', views.logout, name="logout"),
    path('users', views.PartUser, name="PartUser"),
    path('nam\'ser/live',views.live,name="live"),
    path('nam\'ser/matchs/resultat-foot-hier',views.football, name="football"),
    path('nam\'ser/matchs/matchs-demain',views.football_demain, name="football_demain"),
    path('nam\'ser/matchs/matchs-aujourd\hui',views.football_today, name="football_today"),
    path('nam\'ser/parie-match-en-direct',views.parie, name="parie")
]
