import uuid
import random

from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum

from .models import Gateway, Payment

from carts.models import CartItems, CartItemInfo

from subscriptions.models import Subscription

class GatewayView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, ".اول وارد حساب خود شوید")
        gateways = Gateway.objects.filter(is_enable=True)
        cart_items = CartItems.objects.filter(user=request.user)
        total_price = sum(item.quantity * item.place.price for item in cart_items)
        total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
        return render(request, "pay/gateway.html", {"gateways": gateways, "total_price": total_price, "total_quantity":total_quantity, 'cart_items':cart_items})

    def post(self, request):
        gateways = Gateway.objects.filter(is_enable=True)
        cart_items = CartItems.objects.filter(user=request.user)
        total_price = sum(item.quantity * item.place.price for item in cart_items)
        total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0

        dargah = request.POST.get('dargah')  
        if not dargah:
            messages.error(request, ".لطفاً یک درگاه پرداخت انتخاب کنید")
            return render(request, "pay/gateway.html", {"gateways": gateways, "total_price":total_price, "total_quantity":total_quantity, "cart_items":cart_items})
        
        return redirect("payment", dargah) 


class PaymentView(View):
    def get(self, request, dargah):
        cart_items = CartItems.objects.filter(user=request.user)
        total_price = sum(item.quantity * item.place.price for item in cart_items)
        cart_info = CartItemInfo.objects.filter(user=request.user)
        st = random.choices([10,30], weights=[2,1], k=1)[0]
        
        try:
            gateway = Gateway.objects.get(title=dargah, is_enable=True)
        except Gateway.DoesNotExist:
            messages.error(request, "درگاه در دسترس نیست.")
            return redirect('infos')
        
        payment = Payment.objects.create(
            user=request.user,
            gateway=gateway,
            price=total_price,
            phone_number=request.user.phone_number,
            token=str(uuid.uuid4())
        )
        payment.items.set(cart_info)

        callback_url = f"http://127.0.0.1:8000/pay/{gateway.title}/" 

        return render(request, 'pay/payment.html', {
            'token': payment.token,
            'callback_url': callback_url,
            'gateway': gateway,
            'status': st
        })
    def post(self, request, dargah):
        st = request.POST.get("status")
        token = request.POST.get("token")

        try:
            payment = Payment.objects.get(token=token)
        except Payment.DoesNotExist:
            messages.error(request, ".پرداخت یافت نشد")
            return redirect('gateway')

        if st == '10':
            payment.status = Payment.STATUS_PAID
            payment.save()

            for item in payment.items.all():
                if not Subscription.objects.filter(user=payment.user, items=item).exists():
                    Subscription.objects.create(
                        user=payment.user,
                        items=item
                    )

            CartItems.objects.filter(user=request.user).delete()

            messages.success(request, ".با موفقیت انجام شد")
            return render(request, "pay/success.html", {"status": payment.status})

        elif st == '30':
            Payment.objects.filter(user=request.user).delete()
            # CartItems.objects.filter(user=request.user).delete()
            CartItemInfo.objects.filter(user=request.user).delete()
            messages.error(request, "پرداخت توسط کاربر لغو شد")
            return redirect('place-view')