from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ContactUsForm

class ContactUsFormView(View):
    def get(self, request):
        form = ContactUsForm()
        return render(request, "contacts/contact_form.html", {"form": form})

    def post(self, request):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "پیام شما با موفقیت ارسال شد.")
            return redirect("place-view")
        else:
            messages.error(request, "لطفاً اطلاعات خود را بررسی کنید.")
        return render(request, "contacts/contact_form.html", {"form": form})
