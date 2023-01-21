from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from django.contrib import auth
from decimal import Decimal
from main import models
from main import forms

# Create your tests here.

class TestPage(TestCase):
	def test_home_page_works(self):
		response = self.client.get(reverse('home'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')
		self.assertContains(response, 'BookTime')

	def test_about_us_page_works(self):
		response = self.client.get(reverse('about_us'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'BookTime')
		self.assertTemplateUsed(response, 'about_us.html')

	def test_contact_us_page_works(self):
		response = self.client.get(reverse('contact_us'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'contact_form.html')
		self.assertContains(response, 'BookTime')
		self.assertIsInstance(
			response.context['form'], forms.ContactForm
		)

	def test_products_page_returns_active(self):
		models.Product.objects.create(
			name='The cathedral and the bazaar',
			slug='cathedral-bazaar',
			price=Decimal('10.00'),
		)
		models.Product.objects.create(
			name='A Tale of Two Cities',
			slug='tale-two-cities',
			price=Decimal('2.00'),
			active=False,
		)
		response = self.client.get(
			reverse('products', kwargs={'tag': 'all'})
		)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'BookTime')
		product_list = models.Product.objects.active().order_by('name')
		self.assertEqual(
			list(response.context['object_list']),
			list(product_list),
		)

	def test_products_page_filters_by_tags_and_active(self):
		cb = models.Product.objects.create(
			name='The cathedral and the bazaar',
			slug='cathedral-bazaar',
			price=Decimal('10.00'),
		)
		cb.tags.create(name='Open source', slug='opensource')
		models.Product.objects.create(
			name='Microsoft Windows guide',
			slug='microsoft-windows-guide',
			price=Decimal('12.00'),
		)
		response = self.client.get(
			reverse('products', kwargs={'tag': 'opensource'})
		)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'BookTime')

		product_list = (
			models.Product.objects.active()
			.filter(tags__slug='opensource')
			.order_by('name')
		)
		self.assertEqual(
			list(response.context['object_list']),
			list(product_list),
		)

	def test_user_signup_page_loads_correctly(self):
		response = self.client.get(reverse('signup'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'signup.html')
		self.assertContains(response, 'BookTime')
		self.assertIsInstance(
			response.context['form'],
			forms.UserCreationForm
		)

	def test_user_signup_page_submission_works(self):
		post_data = {
			'email': 'user@domain.com',
			'password1': 'abcabcabc',
			'password2': 'abcabcabc',
		}
		with patch.object(
			forms.UserCreationForm,
			'send_mail'
		) as mock_send:
			response = self.client.post(
				reverse('signup'),
				post_data
			)
		self.assertEqual(response.status_code, 302)
		self.assertTrue(
			models.User.objects.filter(email='user@domain.com').exists()
		)
		self.assertTrue(auth.get_user(self.client).is_authenticated)
		mock_send.assert_called_once()
