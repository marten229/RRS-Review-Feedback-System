from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
#from UserManagement.models import User
from .models import Restaurant, Bewertung
from ReservationManagement.models import Reservation

User = get_user_model()

class BewertungViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.client.login(username='testuser', password='12345')

    def test_bewertung_abgeben_view_get(self):
        response = self.client.get(reverse('bewertung_abgeben', args=[self.restaurant.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bewertung_formular.html')
        self.assertContains(response, 'Bewertung abgeben')

    def test_bewertung_abgeben_view_post_valid(self):
        response = self.client.post(reverse('bewertung_abgeben', args=[self.restaurant.pk]), {
            'bewertung_gesamt': 4,
            'bewertung_service': 4,
            'bewertung_essen': 4,
            'bewertung_ambiente': 4,
            'mit_wem': 'familie',
            'anlass': 'abendessen',
            'kommentar': 'Great experience!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Bewertung.objects.count(), 1)
        self.assertEqual(Bewertung.objects.first().kommentar, 'Great experience!')

    def test_bewertung_abgeben_view_post_invalid(self):
        response = self.client.post(reverse('bewertung_abgeben', args=[self.restaurant.pk]), {
            'bewertung_gesamt': 4,
            'bewertung_service': 4,
            'bewertung_essen': 4,
            'bewertung_ambiente': 4,
            'mit_wem': 'invalid_choice',  # Invalid choice to test form validation
            'anlass': 'abendessen',
            'kommentar': 'Great experience!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'mit_wem', 'Select a valid choice. invalid_choice is not one of the available choices.')

class DankeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.client.login(username='testuser', password='12345')

    def test_danke_view(self):
        response = self.client.get(reverse('danke', args=[self.restaurant.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'danke.html')
        self.assertContains(response, 'Danke für Ihre Bewertung!')

class RestaurantBewertungenViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.bewertung = Bewertung.objects.create(
            restaurant=self.restaurant, user=self.user, bewertung_gesamt=4,
            bewertung_service=4, bewertung_essen=4, bewertung_ambiente=4,
            mit_wem='familie', anlass='abendessen', kommentar='Great experience!'
        )
        self.client.login(username='testuser', password='12345')

    def test_restaurant_bewertungen_view(self):
        response = self.client.get(reverse('restaurant_bewertungen', args=[self.restaurant.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant_bewertungen.html')
        self.assertContains(response, 'Bewertungen für Test Restaurant')
        self.assertEqual(response.context['durchschnittliche_bewertung_gesamt'], 4.0)

class DeleteBewertungViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.bewertung = Bewertung.objects.create(
            restaurant=self.restaurant, user=self.user, bewertung_gesamt=4,
            bewertung_service=4, bewertung_essen=4, bewertung_ambiente=4,
            mit_wem='familie', anlass='abendessen', kommentar='Great experience!'
        )
        self.client.login(username='testuser', password='12345')

    def test_delete_bewertung_view(self):
        response = self.client.post(reverse('delete_bewertung', args=[self.restaurant.pk, self.bewertung.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Bewertung.objects.count(), 0)
