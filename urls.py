from django.urls import path
from .views import  danke

urlpatterns = [

    path('restaurants/<int:pk>/danke/', danke, name='danke'),
]