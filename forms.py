from django import forms
from .models import Reservation, Bewertung

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'telefon_nummer', 'datum', 'uhrzeit', 'anzahl_an_gästen']


# Bewertung formular

class BewertungForm(forms.ModelForm):
    class Meta:
        model = Bewertung
        fields = ['bewertung_gesamt', 'bewertung_service', 'bewertung_essen', 'bewertung_ambiente', 'mit_wem', 'anlass', 'kommentar']
        widgets = {
            'bewertung_gesamt': forms.RadioSelect,
            'bewertung_service': forms.RadioSelect,
            'bewertung_essen': forms.RadioSelect,
            'bewertung_ambiente': forms.RadioSelect,
            'mit_wem': forms.RadioSelect,
            'anlass': forms.Select,
            'kommentar': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }