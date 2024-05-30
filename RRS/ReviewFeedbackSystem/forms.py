from django import forms
from .models import Reservation, Bewertung

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'telefon_nummer', 'datum', 'uhrzeit', 'anzahl_an_gästen']


# Bewertung formular

class BewertungForm(forms.ModelForm):
    bewertung = forms.CharField(
        label='Wie würden Sie Ihre Erfahrung bewerten?',
        widget=forms.HiddenInput()
    )
    mit_wem = forms.ChoiceField(
        label='Mit wem waren Sie hier?',
        choices=[
            ('geschäftsreise', 'Geschäftsreise'),
            ('als_paar', 'Als Paar'),
            ('familie', 'Familie'),
            ('mit_freunden', 'Mit Freunden'),
            ('alleine', 'Alleine')
        ],
        widget=forms.RadioSelect
    )
    anlass = forms.ChoiceField(
        label='Was war der Anlass Ihres Besuchs?',
        choices=[
            ('frühstück', 'Frühstück'),
            ('brunch', 'Brunch'),
            ('mittagessen', 'Mittagessen'),
            ('abendessen', 'Abendessen'),
            ('dessert', 'Dessert'),
            ('kaffee_oder_tee', 'Kaffee oder Tee')
        ],
        widget=forms.Select
    )
    kommentar = forms.CharField(
        label='Bewertung',
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 40, 'placeholder': 'Bewertungstipps'})
    )

    class Meta:
        model = Bewertung
        fields = ['bewertung', 'mit_wem', 'anlass', 'kommentar']