from django.urls import path
from .views import RestaurantListView, RestaurantDetailView, create_reservation, bewertung_abgeben, danke, restaurant_bewertungen

urlpatterns = [
    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurants/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('restaurants/<int:pk>/reservation/', create_reservation, name='create-reservation'),
    path('restaurants/<int:pk>/bewertung/', bewertung_abgeben, name='create-bewertung'),
    path('restaurants/<int:pk>/danke/', danke, name='danke'),
    path('restaurants/<int:pk>/bewertungen/', restaurant_bewertungen, name='restaurant-bewertungen'),
]
