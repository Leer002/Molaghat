from django.urls import path

from .views import ContactUsFormView

urlpatterns = [
    path("contact/", ContactUsFormView.as_view(), name="contact")
]
