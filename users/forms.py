from django import forms
from django.contrib.auth.password_validation import validate_password

from .models import User, UserProfile

from utils.validators import validate_phone_number

class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=40)
    email = forms.EmailInput()
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput)
    # phone_number = forms.IntegerField(validators=[validate_phone_number])

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "phone_number"]
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password2 != password1:
            raise forms.ValidationError("Passwords do not match.")

class UserEditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthdate', 'avatar']  # فیلدهایی که می‌خواهید کاربر ویرایش کند
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),  # برای انتخاب تاریخ
        }

