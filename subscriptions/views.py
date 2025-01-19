from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from .models import Subscription

class SubscriptionView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, "ابتدا وارد حساب کاربری خود شوید.")
            return redirect('login')
        subscription = Subscription.objects.filter(
            user=request.user,
            created_date__lt=Subscription.items.place.event_time
        )
        return render(request, "users/profile.html", {"subscription":subscription})