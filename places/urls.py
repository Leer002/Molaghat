from django.urls import path

from .views import CategoryView, PlaceDetailView, PlaceListView, SearchView

urlpatterns = [
    path('', PlaceListView.as_view(), name="place-view"),
    path('<int:pk>/', PlaceDetailView.as_view(), name="detail"),
    path('search/', SearchView.as_view(), name="search"),
    path('<str:cat>/', CategoryView.as_view(), name="category")
]
