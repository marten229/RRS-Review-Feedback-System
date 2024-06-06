from django import forms
from .models import Reservation, Bewertung

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'telefon_nummer', 'datum', 'uhrzeit', 'anzahl_an_gästen']


# Bewertung formular

class BewertungForm(forms.ModelForm):
    bewertung = forms.ChoiceField(label='Bewertung', choices=[
        ('5', '1'),
        ('4', '2'),
        ('3', '3'),
        ('2', '4'),
        ('1', '5')
    ], widget=forms.RadioSelect)
    kommentar = forms.CharField(label='Kommentar', widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))
    
    class Meta:
        model = Bewertung
        fields = ['bewertung', 'kommentar']
