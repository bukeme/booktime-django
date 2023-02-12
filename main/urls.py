from django.urls import path 
from main import views
from main import models
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth import views as auth_views
from main import forms


urlpatterns = [
	path('about-us/', TemplateView.as_view(template_name='about_us.html'), name='about_us'),
	path('', TemplateView.as_view(template_name='home.html'), name='home'),
	path('contact-us/', views.ContactUsView.as_view(), name='contact_us'),
	path('products/<slug:tag>/', views.ProductListView.as_view(), name='products'),
	path('product/<slug:slug>/', DetailView.as_view(model=models.Product), name='product'),
	path('signup/', views.SignupView.as_view(), name='signup'),
	path(
		'login/',
		auth_views.LoginView.as_view(
			template_name='login.html',
			form_class=forms.AuthenticationForm,
		),
		name='login',
	),
	path('address/', views.AddressListView.as_view(), name='address_list'),
	path('address/create/', views.AddressCreateView.as_view(), name='address_create'),
	path('address/<int:pk>/', views.AddressUpdateView.as_view(), name='address_update'),
	path('address/<int:pk>/delete/', views.AddressDeleteView.as_view(), name='address_delete'),
	path('add_to_basket/', views.add_to_basket, name='add_to_basket',),
	path('basket/', views.manage_basket, name='basket'),
]
