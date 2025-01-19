import random
from kavenegar import *

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)


from .models import User, UserProfile
from .forms import UserRegisterForm, UserEditProfileForm, ChangePasswordForm

from carts.models import UserInfo

from subscriptions.models import Subscription


# api = KavenegarAPI('6C77622F6A2F74544F453672546C365A633755463263644A73537970564A70303054756746493751396D553D')
# params = { 'sender' : '2000660110', 'receptor': '09902111473', 'message' :'.وب سرویس پیام کوتاه کاوه نگار' }
# response = api.sms_send(params)


# class UserRegisterView(View):
#     def get(self, request):
#         form = UserRegisterForm()
#         return render(request, "users/register.html", context={"form":form})
#     def post(self, request):
#         form = UserRegisterForm(request.POST)

#         if form.is_valid():
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("password1")
#             phone_number = form.cleaned_data.get("phone_number")

#             try:
#                 api = KavenegarAPI("6C77622F6A2F74544F453672546C365A633755463263644A73537970564A70303054756746493751396D553D", timeout=20)
#                 params = params
#                 response = response
#                 print(response)
#             except APIException as e: 
#                 print(e)
#             except HTTPException as e: 
#                 print(e)

#             if User.objects.filter(username=username).exists():
#                 messages.error(request, "Username is taken")
#                 return redirect("place-view")
            
#             user_obj = form.save(commit=False)
#             user_obj.set_password(password)
#             user_obj.save()

#             authenticate_user = authenticate(request, username=username, password=password)
#             if authenticate_user is not None:
#                 login(request, authenticate_user)
#                 UserProfile.objects.create(user=user_obj)
#                 return redirect("place-view")
            
#         return render(request, "users/register.html", context={"form":form})

class UserRegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, "users/register.html", context={"form": form})

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            phone_number = form.cleaned_data.get("phone_number")

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is taken")
                return redirect("place-view")
            
            # verification_code = random.randint(10000, 99999)
            # cache.set(phone_number)

            user_obj = form.save(commit=False)
            user_obj.set_password(password)
            user_obj.save()

            authenticate_user = authenticate(request, username=username, password=password)
            if authenticate_user is not None:
                login(request, authenticate_user)
                UserProfile.objects.create(user=user_obj)
                return redirect("place-view")

        return render(request, "users/register.html", context={"form": form})


class UserLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'users/login.html', context={'form': form})
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user_obj = User.objects.filter(username=username).first()
        if not user_obj:
            messages.error(request, "نام کاربری پیدا نشد")
            return redirect("login")  # بازگشت به صفحه ورود
        
        user_obj = authenticate(username=username, password=password)
        if user_obj:
            login(request, user_obj)
            return redirect("place-view")
        
        messages.error(request, "رمز عبور اشتباه است")
        return redirect("login")  # بازگشت به صفحه ورود


class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect("place-view")
    
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        subscriptions = Subscription.objects.filter(user=request.user)
        return render(request, 'users/profile.html', {'profile': user_profile, 'subscriptions':subscriptions})

@method_decorator(login_required, name='dispatch')
class EditProfileView(UpdateView):
    model = UserProfile
    form_class = UserEditProfileForm
    template_name = 'users/edit_profile.html'
    
    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile')


class ChangePasswordView(PasswordChangeView):
    template_name = "users/change_password.html"
    success_url = reverse_lazy("login")
    form_class = ChangePasswordForm

class PasswordReset(PasswordResetView):
    template_name = "users/password_reset_form.html"
    success_url = reverse_lazy("password_reset_done")

class PasswordResetDone(PasswordResetDoneView):
    template_name = "users/password_reset_done.html"
    success_url = reverse_lazy("password_reset_confirm")


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"