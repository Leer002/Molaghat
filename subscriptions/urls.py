from django.urls import path

from .views import SubscriptionView

urlpatterns = [
    path('sub/', SubscriptionView.as_view(), name="subscription")
]
