from django.urls import path

from .views import ProfileView, EditProfileView, UserLoginView, UserLogout, UserRegisterView, ChangePasswordView, PasswordReset, PasswordResetDone, PasswordResetConfirm, PasswordResetComplete

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', UserLogout.as_view(), name="logout"),
    path('edit/', EditProfileView.as_view(), name="edit_profile"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('change/password/', ChangePasswordView.as_view(), name="change-password"),
      path("password_reset/", PasswordReset.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        PasswordResetDone.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirm.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetComplete.as_view(),
        name="password_reset_complete",
    ),
]
