import json
import requests
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, reverse

from orders.models import Order
import my_config


def payment_process(request):
    # Get order id from session
    order_id = request.session.get('order_id')
    # get the order object
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    # zarinpal_request_url = 'https://api.zarinpal.com/pg/v4/payment/request.json'
    zarinpal_request_url = 'https://sandbox.zarinpal.com/pg/v4/payment/request.json'
    request_header = {
        'accept': 'application/json',
        'content-type': 'application/json',
    }
    request_data = {
        'merchant_id': my_config.DJANGO_ZARINPAL_MERCHANT_ID,
        'amount': rial_total_price,
        'description': f'#{order_id}: {order.user.first_name} {order.user.last_name}',
        'callback_url': request.build_absolute_uri(reverse('payment:payment_callback')),
    }
    response = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)

    data = response.json()['data']
    print(data)
    authority = data['authority']
    # authority = "test"
    order.zarinpal_authority = authority
    order.save()

    # https: // zarinpal.com / pg / StartPay
    if 'errors' not in data or len(data['errors']) == 0:
        return redirect(f'https://sandbox.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponse('Error from zarinpal')


def payment_callback(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price

    if payment_status == 'OK':
        request_header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        request_data = {
            'merchant_id': my_config.DJANGO_ZARINPAL_MERCHANT_ID,
            'amount': rial_total_price,
            'authority': payment_authority,
        }
        # 'https://api.zarinpal.com/pg/v4/payment/verify.json',

        response = requests.post(
            'https://sandbox.zarinpal.com/pg/v4/payment/verify.json',
            data=json.dumps(request_data),
            headers=request_header,
        )
        if ('data' in response.json()
                and 'errors' not in response.json()['data']
                or len(response.json()['data']['errors']) == 0):
            data = response.json()['data']
            payment_code = data['code']

            if payment_code == 100:
                order.is_paid = True
                order.zarinpal_ref_id = data['ref_id']
                order.zarinpal_data = data
                order.save()

                return HttpResponse('payment successful')
            elif payment_code == 101:
                return HttpResponse('payment successful but duplicated')
            else:
                error_code = response.json()['errors']['code']
                error_message = response.json()['errors']['message']
                return HttpResponse(f'transaction fail.{error_code} {error_message}')
    else:
        return HttpResponse('transaction fail.')


def payment_process_sandbox(request):
    # Get order id from session
    order_id = request.session.get('order_id')
    # get the order object
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    zarinpal_request_url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json'
    request_header = {
        'accept': 'application/json',
        'content-type': 'application/json',
    }
    request_data = {
        'MerchantID': my_config.DJANGO_ZARINPAL_MERCHANT_ID,
        'Amount': rial_total_price,
        'Description': f'#{order_id}: {order.user.first_name} {order.user.last_name}',
        'CallbackURL': request.build_absolute_uri(reverse('payment:payment_callback')),
    }
    response = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)

    data = response.json()
    print(data)
    authority = data['Authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' not in data or len(data['errors']) == 0:
        print(f'https://sandbox.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
        return redirect(f'https://sandbox.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponse('Error from zarinpal')


def payment_callback_sandbox(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price

    if payment_status == 'OK':
        request_header = {
            'accept': 'application/json',
            'content-type': 'application/json',
        }
        request_data = {
            'MerchantID': my_config.DJANGO_ZARINPAL_MERCHANT_ID,
            'Amount': rial_total_price,
            'Authority': payment_authority,
        }

        response = requests.post(
            'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json',
            data=json.dumps(request_data),
            headers=request_header,
        )
        print(response.json())
        if 'errors' not in response.json():
            data = response.json()

            payment_code = data['Status']
            print(payment_code)
            if payment_code == 100:
                order.is_paid = True
                order.zarinpal_ref_id = data['RefID']
                order.zarinpal_data = data
                order.save()

                return HttpResponse('payment successful')
            elif payment_code == 101:
                return HttpResponse('payment successful but duplicated')
            else:
                error_code = response.json()['RefID']
                error_message = response.json()
                return HttpResponse(f'transaction fail.{error_code} {error_message}')
    else:
        return HttpResponse('transaction faillllllllllllll.')
