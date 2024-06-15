from django.db import models
from django.utils import timezone
from RestaurantManagement.models import Restaurant
from UserManagement.models import User
from ReservationManagement.models import Reservation
    
##Bewerung
class Bewertung(models.Model):
    BEWERTUNG_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    MIT_WEM_CHOICES = (
        ('geschäftsreise', 'Geschäftsreise'),
        ('als_paar', 'Als Paar'),
        ('familie', 'Familie'),
        ('mit_freunden', 'Mit Freunden'),
        ('alleine', 'Alleine'),
    )

    ANLASS_CHOICES = (
        ('frühstück', 'Frühstück'),
        ('brunch', 'Brunch'),
        ('mittagessen', 'Mittagessen'),
        ('abendessen', 'Abendessen'),
        ('dessert', 'Dessert'),
        ('kaffee_oder_tee', 'Kaffee oder Tee'),
    )

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='bewertungen')
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='bewertungen', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bewertungen', default=1)
    bewertung_gesamt = models.PositiveSmallIntegerField(choices=BEWERTUNG_CHOICES, default=3)
    bewertung_service = models.PositiveSmallIntegerField(choices=BEWERTUNG_CHOICES, default=3)
    bewertung_essen = models.PositiveSmallIntegerField(choices=BEWERTUNG_CHOICES, default=3)
    bewertung_ambiente = models.PositiveSmallIntegerField(choices=BEWERTUNG_CHOICES, default=3)
    mit_wem = models.CharField(max_length=20, choices=MIT_WEM_CHOICES, null=True)
    anlass = models.CharField(max_length=20, choices=ANLASS_CHOICES, null=True)
    kommentar = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Bewertung für : {self.bewertung_gesamt}"