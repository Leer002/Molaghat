from django.urls import path

from .views import GatewayView, PaymentView

urlpatterns = [
    path("gateway/", GatewayView.as_view(), name="gateway"),
    path("<str:dargah>/", PaymentView.as_view(), name="payment")
]
