from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .cart_modul import Cart
from product.models import Product
from .models import Order, OrderItem


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


class OrderDetailView(View):
    def get(self,request,pk):
        order = get_object_or_404(Order,id=pk)
        return render(request, 'cart/order_detail.html', {'order': order})

class OrderCreationView(View):
    def get(self,request):
        cart=Cart(request)
        order=Order.objects.create(user=request.user, total_price=cart.total_price())
        for item in cart:
            OrderItem.objects.create(order=order,product=item['product'],color=item['color'],size=item['size'],quantity=item['quantity'],price=item['price'])
        cart.remove_cart()
        return redirect('cart:order_detail',order.id)