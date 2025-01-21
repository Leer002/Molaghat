from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import PasswordChangeForm

from .models import User, UserProfile

class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=40)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "phone_number"]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password2 != password1:
            raise forms.ValidationError(".رمزهای عبور مطابقت ندارند")


class UserEditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthdate', 'avatar'] 
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            {"placeholder": "گذرواژه فعلی", "id": "old_password"}
        )
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            {"placeholder": "گذرواژه جدید", "id": "new_password1"}
        )
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            {"placeholder": "تکرار گذرواژه", "id": "new_password2"}
        )
    )

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        if len(new_password1) < 7:
            raise ValidationError("گذروازه باید بیشتر از 7 کاراکتر باشد")
        return new_password1
    
    def clean_new_password2(self):
        new_password2 = self.cleaned_data.get('new_password2')
        if len(new_password2) < 7:
            raise ValidationError("گذروازه باید بیشتر از 7 کاراکتر باشد")
        return new_password2

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
                "گذرواژه فعلی تان اشتباه وارد شد. لطفا دوباره تلاش کنید"
            )
        return old_password
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password2 != password1:
            raise ValidationError(".رمزهای عبور مطابقت ندارند")
    
