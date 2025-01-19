from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.db.models import Sum


from .models import UserInfo, CartItems

from places.models import Place

class CartItemView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, "شما باید ابتدا وارد شوید.")
            return redirect("login")

        cart_items = CartItems.objects.filter(user=request.user, is_purchased=False)
        total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_price = sum(item.quantity * item.place.price for item in cart_items)

        return render(request, "carts/cart.html", {
            "total_price": total_price,
            "total_quantity": total_quantity,
            "items_list": cart_items
        })

class CartItemAddView(View):
    def post(self, request, place_id):
        if not request.user.is_authenticated:
            messages.error(request, "شما باید ابتدا وارد شوید.")
            return redirect("login")
        place = get_object_or_404(Place, id=place_id)
        cart_item, created = CartItems.objects.get_or_create(user=request.user, place=place)
        cart_item.quantity += 1
        cart_item.save()

        messages.success(request, "کالا به سبد خرید اضافه شد.")
        return redirect("cart-view")

class CartItemRemoveView(View):
    def post(self, request, place_id):
        cart_item = get_object_or_404(CartItems, user=request.user, place_id=place_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            messages.success(request, "کالا از سبد خرید حذف شد.")
        else:
            cart_item.delete()
            messages.success(request, "کالا از سبد خرید حذف شد.")

        return redirect("cart-view")

class CheckOut(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, "شما باید ابتدا وارد شوید.")
            return redirect("login")
        cart_items = CartItems.objects.filter(user=request.user)

        if not cart_items.exists(): 
            return redirect("cart-view")
                
        user_info = UserInfo.objects.filter(user=request.user).first() if request.user.is_authenticated else None
        
        return render(request, "carts/checkout.html", {
            "cart_items": cart_items,
            "user_info": user_info,
        })

    def post(self, request):
        if not request.user.is_authenticated:
            messages.error(request, "شما باید ابتدا وارد شوید.")
            return redirect("login")

        address = request.POST.get("address")
        phone_number = request.POST.get("phone_number")
        
        if not address or not phone_number:
            messages.error(request, "آدرس و شماره تلفن الزامی است.")
            return redirect("checkout-view")

        user_info, created = UserInfo.objects.get_or_create(user=request.user)
        user_info.address = address
        user_info.phone_number = phone_number
        user_info.save()


        messages.success(request, "تسویه حساب با موفقیت انجام شد.")
        return redirect("cart-view")

class InfosView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, "شما باید ابتدا وارد شوید.")
            return redirect("login")

        user_info = UserInfo.objects.filter(user=request.user).first()
        cart_items = CartItems.objects.filter(user=request.user)
        total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_price = sum(item.quantity * item.place.price for item in cart_items)
        
        return render(request, 'carts/infos.html', {
            'name': request.user.username,
            'phone': user_info.phone_number if user_info else '',
            'address': user_info.address if user_info else '',
            'cart_items':cart_items,
            'total_price':total_price,
            'total_quantity':total_quantity,
            'status': 'لطفاً اطلاعات خود را وارد کنید.' if not user_info else ''
        })

    def post(self, request):
        if not request.user.is_authenticated:
            messages.error(request, "شما باید ابتدا وارد شوید.")
            return redirect("login")
        
        
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        user_info, created = UserInfo.objects.get_or_create(user=request.user)

        if phone:
            user_info.phone_number = phone
        if address:
            user_info.address = address
        
        user_info.save()
        messages.success(request, "اطلاعات شما با موفقیت به‌روزرسانی شد.")
        return redirect("infos")
