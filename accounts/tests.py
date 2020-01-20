from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import dashboardView, profile, registerView
# Create your tests here.

class TestUrls(SimpleTestCase):

	def test_dashboard_view(self):
		url = reverse('home')
		self.assertEquals(resolve(url).func, dashboardView)

	def test_register_view(self):
		url = reverse('register')
		self.assertEquals(resolve(url).func, registerView)

	def test_profile_view(self):
		url = reverse('profile')
		self.assertEquals(resolve(url).func, profile)
