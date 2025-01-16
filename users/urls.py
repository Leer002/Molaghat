from django.urls import path

from .views import ProfileView, EditProfileView, UserLoginView, UserLogout, UserRegisterView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', UserLogout.as_view(), name="logout"),
    path('edit/', EditProfileView.as_view(), name="edit_profile"),
    path('profile/', ProfileView.as_view(), name="profile")
]
