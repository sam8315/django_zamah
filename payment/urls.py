from django.urls import path, include

from .views import *


app_name = 'payment'

urlpatterns = [
    path('process/', payment_process_sandbox, name='payment_process'),
    path('callback/', payment_callback_sandbox, name='payment_callback'),

]
