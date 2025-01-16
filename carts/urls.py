from django.urls import path

from .views import CartItemAddView, CartItemRemoveView, CartItemView, CheckOut, InfosView

urlpatterns = [
    path('cart/', CartItemView.as_view(), name="cart-view"),
    path('cart/add/<int:place_id>/', CartItemAddView.as_view(), name="cart-add"),
    path('cart/remove/<int:place_id>/', CartItemRemoveView.as_view(), name="cart-remove"),
    path('checkout/', CheckOut.as_view(), name="checkout"),
    path('info/', InfosView.as_view(), name="infos")
]
