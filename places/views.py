
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.utils import timezone

from .models import Category, Place, File

class PlaceListView(View):
    def get(self, request):
        places = Place.objects.filter(is_enable=True, event_date=timezone.now())
        categories = Category.objects.all()
        files = File.objects.all()
        # total_quantity
        # pagination
        return render(request, "places/base.html", {"places":places, "categories":categories, "files":files})
    
class PlaceDetailView(View):
    def get(self, request, pk):
        place = get_object_or_404(Place, pk=pk)
        like = place.like
        try:
            file = File.objects.get(place=place)
        except File.DoesNotExist:
            file = None

        return render(request, "places/detail.html", {"place":place, "file":file, "like":like})
    def post(self, request, pk):
        place = get_object_or_404(Place, pk=pk)
        place.like += 1
        place.save()
        return redirect("detail", pk=pk)


class SearchView(View):
    def get(self, request):
        query = request.GET.get("query", "")
        search_places = Place.objects.filter(place_name__icontains=query) if query else Place.objects.all()
        
        return render(request, "places/search.html", {"search_places": search_places, "query": query})

class CategoryView(View):
    def get(self, request, cat):
        cat = cat.replace("-", " ")
        category = get_object_or_404(Category, title=cat)
        
        filter_price = request.GET.get("filter_price")
        
        category_places = Place.objects.filter(category=category)
        
        if filter_price == "max":
            category_places = category_places.order_by("-price")
        else:
            category_places = category_places.order_by("price")

        if not category_places.exists():
            messages.warning(request, "No places found in this category.")
        
        return render(request, "places/category.html", {
            "category": category,
            "category_places": category_places,
            "filter_price": filter_price
        })
