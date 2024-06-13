from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Count
from django.views.generic import ListView, DetailView
from .models import Restaurant, User, Bewertung
from .forms import ReservationForm, BewertungForm
from UserManagement.models import User
from django.contrib.auth.decorators import login_required

class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurant_list.html'
    context_object_name = 'restaurants'

    def get_queryset(self):
        return Restaurant.objects.all()

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurant_detail.html'
    context_object_name = 'restaurant'

    def get_object(self):
        restaurant_id = self.kwargs.get('pk')
        return get_object_or_404(Restaurant, pk=restaurant_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = self.get_object()
        bewertungen = Bewertung.objects.filter(restaurant=restaurant)
        
        # Berechnen Sie die durchschnittliche Bewertung für jedes Kriterium
        durchschnittliche_bewertung_gesamt = bewertungen.aggregate(Avg('bewertung_gesamt'))['bewertung_gesamt__avg'] or 0
        durchschnittliche_bewertung_service = bewertungen.aggregate(Avg('bewertung_service'))['bewertung_service__avg'] or 0
        durchschnittliche_bewertung_essen = bewertungen.aggregate(Avg('bewertung_essen'))['bewertung_essen__avg'] or 0
        durchschnittliche_bewertung_ambiente = bewertungen.aggregate(Avg('bewertung_ambiente'))['bewertung_ambiente__avg'] or 0
        anzahl_bewertungen = bewertungen.count()

        volle_sterne = int(durchschnittliche_bewertung_gesamt)
        halber_stern = durchschnittliche_bewertung_gesamt - volle_sterne >= 0.5
        
        context['durchschnittliche_bewertung_gesamt'] = durchschnittliche_bewertung_gesamt
        context['durchschnittliche_bewertung_service'] = durchschnittliche_bewertung_service
        context['durchschnittliche_bewertung_essen'] = durchschnittliche_bewertung_essen
        context['durchschnittliche_bewertung_ambiente'] = durchschnittliche_bewertung_ambiente
        context['anzahl_bewertungen'] = anzahl_bewertungen
        context['volle_sterne'] = volle_sterne
        context['halber_stern'] = halber_stern
        context['bewertungen'] = bewertungen
        
        return context

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

@login_required
def bewertung_abgeben(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        form = BewertungForm(request.POST)
        if form.is_valid():
            bewertung = form.save(commit=False)
            bewertung.restaurant = restaurant
            bewertung.user = request.user
            bewertung.save()
            return redirect('danke', pk=pk)
        else:
            print("Form is not valid", form.errors)
    else:
        form = BewertungForm()
    return render(request, 'bewertung_formular.html', {'form': form, 'restaurant': restaurant})

@login_required
def danke(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    return render(request, 'danke.html', {'restaurant': restaurant, 'restaurant_pk': pk})

def restaurant_bewertungen(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    bewertungen = Bewertung.objects.filter(restaurant=restaurant)
    
    durchschnittliche_bewertung_gesamt = bewertungen.aggregate(Avg('bewertung_gesamt'))['bewertung_gesamt__avg'] or 0
    durchschnittliche_bewertung_service = bewertungen.aggregate(Avg('bewertung_service'))['bewertung_service__avg'] or 0
    durchschnittliche_bewertung_essen = bewertungen.aggregate(Avg('bewertung_essen'))['bewertung_essen__avg'] or 0
    durchschnittliche_bewertung_ambiente = bewertungen.aggregate(Avg('bewertung_ambiente'))['bewertung_ambiente__avg'] or 0
    anzahl_bewertungen = bewertungen.count()

    volle_sterne = int(durchschnittliche_bewertung_gesamt)
    halber_stern = durchschnittliche_bewertung_gesamt - volle_sterne >= 0.5
    
    return render(request, 'restaurant_bewertungen.html', {
        'restaurant': restaurant,
        'bewertungen': bewertungen,
        'durchschnittliche_bewertung_gesamt': durchschnittliche_bewertung_gesamt,
        'durchschnittliche_bewertung_service': durchschnittliche_bewertung_service,
        'durchschnittliche_bewertung_essen': durchschnittliche_bewertung_essen,
        'durchschnittliche_bewertung_ambiente': durchschnittliche_bewertung_ambiente,
        'anzahl_bewertungen': anzahl_bewertungen,
        'volle_sterne': volle_sterne,
        'halber_stern': halber_stern
    })

def delete_bewertung(request, bewertung_id):
    bewertung = get_object_or_404(Bewertung, id=bewertung_id)
    restaurant_id = bewertung.restaurant.id
    bewertung.delete()
    return redirect('restaurant-bewertungen', pk=restaurant_id)
