from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Count
from django.views.generic import ListView, DetailView
from .models import Restaurant, User, Bewertung
from .forms import ReservationForm, BewertungForm
from UserManagement.models import User
from django.contrib.auth.decorators import login_required
from UserManagement.decorators import role_and_restaurant_required

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

@login_required
@role_and_restaurant_required(['administrator', 'restaurant_owner', 'restaurant_staff'])
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

def delete_bewertung(request, pk, bewertung_id):
    bewertung = get_object_or_404(Bewertung, id=bewertung_id)
    bewertung.delete()
    return redirect('restaurant-reviews', pk=pk)
