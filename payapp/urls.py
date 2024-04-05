from django.urls import path
from . import views
urlpatterns = [
    path('payapp/send', views.send_money, name="send"),
    path('payapp/request', views.request_money, name='request'),
    path('payapp/process_pending_transactions', views.process_pending, name='pending'),

]