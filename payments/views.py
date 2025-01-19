import uuid
import requests

from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum

from .models import Gateway, Payment

from carts.models import CartItems

from subscriptions.models import Subscription

class GatewayView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, "!اول وارد حساب خود شوید")
        gateways = Gateway.objects.filter(is_enable=True)
        cart_items = CartItems.objects.filter(user=request.user, is_purchased=False)
        total_price = sum(item.quantity * item.place.price for item in cart_items)
        total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
        return render(request, "payments/gateway.html", {"gateways": gateways, "total_price": total_price, "total_quantity":total_quantity})

    def post(self, request):
        gateways = Gateway.objects.filter(is_enable=True)
        total_price = sum(item.quantity * item.place.price for item in CartItems.objects.filter(user=request.user))

        dargah = request.POST.get('dargah')  
        if not dargah:
            messages.error(request, "لطفاً یک درگاه پرداخت انتخاب کنید.")
            return render(request, "payments/gateway.html", {"gateways": gateways, "total_price": total_price})
        
        return redirect("payment", dargah) 


class PaymentView(View):
    def get(self, request, dargah):
        cart_items = CartItems.objects.filter(user=request.user, is_purchased=False)
        total_price = sum(item.quantity * item.place.price for item in cart_items)
        
        try:
            gateway = Gateway.objects.get(title=dargah, is_enable=True)
        except Gateway.DoesNotExist:
            messages.error(request, "درگاه در دسترس نیست.")
            return redirect('gateway')

        payment = Payment.objects.create(
            user=request.user,
            gateway=gateway,
            price=total_price,
            phone_number=request.user.phone_number,
            token=str(uuid.uuid4()),
            items = cart_items.first()
        )

        callback_url = f"http://127.0.0.1:8000/pay/{gateway.title}/" 

        return render(request, 'payments/payment.html', {
            'token': payment.token,
            'callback_url': callback_url,
            'gateway': gateway
        })
    def post(self, request, dargah):
        st = request.POST.get("status")
        token = request.POST.get("token")

        try:
            payment = Payment.objects.get(token=token)
        except Payment.DoesNotExist:
            messages.error(request, ".پرداخت یافت نشد")
            return redirect('gateway')

        # If there really was a payment gateway:
        # if st != '10': 
        #     payment.status = Payment.STATUS_CANCELED
        #     payment.save()
        #     messages.error(request, ".پرداخت توسط کاربر لغو شد")

        # r = requests.post("bank_verify_url", data={"token": token})
        # if r.status_code // 100 != 2:
        #     payment.status = Payment.STATUS_ERROR
        #     payment.save()
        #     messages.error(request, ".پرداخت تایید نشد")

        # payment.status = Payment.STATUS_PAID
        # payment.save()
        # -------------------------------------

        if st == '10':
            payment.status = Payment.STATUS_PAID
            payment.save()

            subscription = Subscription.objects.create(
                user=payment.user,
                items=payment.items
            )
            CartItems.objects.filter(user=request.user).update(is_purchased=True)

            messages.success(request, ".با موفقیت انجام شد")
            return render(request, "payments/success.html", {"subscription": subscription, "status": payment.status})

        else:
            payment.status = Payment.STATUS_CANCELED
            payment.save()
            messages.error(request, "پرداخت توسط کاربر لغو شد")
            return redirect('place-view')  
            

    
