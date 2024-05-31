from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Restaurant, User
from .forms import ReservationForm, BewertungForm
from .models import Bewertung

# View für die Übersicht aller Restaurants
class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurant_list.html'  # Pfad zur Template-Datei für die Übersicht
    context_object_name = 'restaurants'

    def get_queryset(self):
        return Restaurant.objects.all()

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurant_detail.html'  # Pfad zur Template-Datei für die Detailansicht
    context_object_name = 'restaurant'

    def get_object(self):
        restaurant_id = self.kwargs.get('pk')
        return Restaurant.objects.get(pk=restaurant_id)
    
class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurant_detail.html'  # Pfad zur Template-Datei für die Detailansicht
    context_object_name = 'restaurant'

    def get_object(self):
        restaurant_id = self.kwargs.get('pk')
        return Restaurant.objects.get(pk=restaurant_id)

def create_reservation(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    dummy_user, created = User.objects.get_or_create(username='dummy_user', defaults={'email': 'dummy@example.com', 'password': 'dummy_password'})
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.restaurant = restaurant
            reservation.user = dummy_user
            reservation.save()
            return redirect('restaurant-detail', pk=restaurant.pk)
    else:
        form = ReservationForm()
    return render(request, 'create_reservation.html', {'form': form, 'restaurant': restaurant})




##bewertun abgeben
def bewertung_abgeben(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        form = BewertungForm(request.POST)
        if form.is_valid():
            bewertung = form.save(commit=False)
            bewertung.restaurant = restaurant
            bewertung.save()
            return redirect('danke', pk=pk)
        else:
            print("Form is not valid", form.errors)
    else:
        form = BewertungForm()
    return render(request, 'bewertung_formular.html', {'form': form, 'restaurant': restaurant})

def danke(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    return render(request, 'danke.html', {'restaurant': restaurant, 'restaurant_pk': pk})



from django.shortcuts import render, get_object_or_404
from .models import Restaurant, Bewertung

def restaurant_bewertungen(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    bewertungen = Bewertung.objects.filter(restaurant=restaurant)
    return render(request, 'restaurant_bewertungen.html', {'restaurant': restaurant, 'bewertungen': bewertungen})

