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
        fields = ['bewertung', 'mit_wem', 'anlass', 'kommentar']
        widgets = {
            'bewertung': forms.RadioSelect,
            'mit_wem': forms.RadioSelect,
            'anlass': forms.Select,
            'kommentar': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }