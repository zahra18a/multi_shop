from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from account.models import Address
from .cart_modul import Cart
from product.models import Product
from .models import Order, OrderItem, DiscountCode
from django.conf import settings
import requests
import json


class CartDetailView(View):
    def get(self,request):
        cart = Cart(request)
        return render(request, 'cart/cart_detail.html', {'cart': cart})


class CartAddView(View):
    def post(self,request,pk):
        size, color, quantity=request.POST.get('size','empty'), request.POST.get('color', 'empty'), request.POST.get('quantity')
        product=get_object_or_404(Product,pk=pk)
        cart=Cart(request)
        cart.add_item_to_cart(product,quantity,color,size)
        return redirect('cart:cart_detail')


class CartRemoveView(View):
    def get(self,request,id):
        cart=Cart(request)
        cart.delete_item_from_cart(id)
        return redirect('cart:cart_detail')


class OrderDetailView(LoginRequiredMixin,View):
    def get(self,request,pk):
        order = get_object_or_404(Order,id=pk)
        return render(request, 'cart/order_detail.html', {'order': order})

class OrderCreationView(LoginRequiredMixin,View):
    def get(self,request):
        cart=Cart(request)
        order=Order.objects.create(user=request.user, total_price=cart.total_price())
        for item in cart:
            OrderItem.objects.create(order=order,product=item['product'],color=item['color'],size=item['size'],quantity=item['quantity'],price=item['price'])
        cart.remove_cart()
        return redirect('cart:order_detail',order.id)


class ApplyDiscountView(LoginRequiredMixin,View):
    def post(self,request,pk):
        code = request.POST.get('discount_code')
        order = get_object_or_404(Order,id=pk)
        discount_code = get_object_or_404(DiscountCode,code=code)
        if discount_code.quantity == 0:
            return redirect('cart:order_detail',order.id)
        order.total_price -= order.total_price * (discount_code.discount / 100)
        order.save()
        discount_code.quantity -= 1
        discount_code.save()
        return redirect('cart:order_detail',order.id)



# ? sandbox merchant
# if settings.SANDBOX:
#     sandbox = 'sandbox'
# else:
#     sandbox = 'www'

ZP_API_REQUEST = f"https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://sandbox.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8080/cart/verify/'


class SendRequestView(View):
    def post(self,request, pk):
        order = get_object_or_404(Order,id=pk, user=request.user)
        address = get_object_or_404(Address,id=request.POST.get('address'))
        # print('5555',request.POST.get('address'))
        order.save()
        data = {
            "MerchantID": '',
            "Amount": order.total_price,
            "Description": description,
            "Phone": request.user.phone,
            "CallbackURL": CallbackURL,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        try:
            response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                            'authority': response['Authority']}
                else:
                    return {'status': False, 'code': str(response['Status'])}
            return response

        except requests.exceptions.Timeout:
            return {'status': False, 'code': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'status': False, 'code': 'connection error'}

