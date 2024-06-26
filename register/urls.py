from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name="register"),
    path('', views.home, name="home"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('admin_view/', views.admin_view, name="admin_view"),

]
