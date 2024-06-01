from django.db import models

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100)
    telefon_nummer = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField()
    öffnungszeiten = models.CharField(max_length=100)
    beschreibung = models.TextField()
    image = models.ImageField(upload_to='restaurant_images', blank=True)

    def __str__(self):
        return self.name
    
class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.username

class Reservation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    telefon_nummer = models.CharField(max_length=15)
    datum = models.DateField()
    uhrzeit = models.TimeField()
    anzahl_an_gästen = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.datum} at {self.uhrzeit}"
    
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

    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='bewertungen')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bewertungen' , default=1)
    bewertung = models.PositiveSmallIntegerField(choices=BEWERTUNG_CHOICES, default=3)
    mit_wem = models.CharField(max_length=20, choices=MIT_WEM_CHOICES)
    anlass = models.CharField(max_length=20, choices=ANLASS_CHOICES)
    kommentar = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Bewertung für : {self.bewertung}"