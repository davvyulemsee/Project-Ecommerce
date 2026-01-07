from django_daraja.mpesa.core import MpesaClient
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

mpesa = Mpesa(
    app_key = "ILUSe7bWQeFZlE2mU6MDLPUNtKqC77grtpdDah5P933Z5eHu",
    app_secret = "QCXrygK078rBI2GHpcBNur4VUk5bFtmIpieushrTHJwFZKhApdFu7ZAMLvgwvoNC",
    env = "sandbox",
)



def pay_mpesa(request):
    phone = request.POST['0718131313']
    amount = request.POST['100']
    response = mpesa.stk_push(phone, amount,'E-shop payment', "Order_123")
    return JsonResponse({'message':"Payment Initiated!"})