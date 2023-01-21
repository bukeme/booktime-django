from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.


class ProductTagManager(models.Manager):
	def get_by_natural_key(self, slug):
		return self.get(slug=slug)

class ProductTag(models.Model):
	objects = ProductTagManager()
	name = models.CharField(max_length=32)
	slug = models.SlugField(max_length=48)
	description = models.TextField(blank=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.name 

	def natural_key(self):
		return (self.slug,)


class ActiveManager(models.Manager):
	def active(self):
		return self.filter(active=True)

class Product(models.Model):
	objects = ActiveManager()
	tags = models.ManyToManyField(ProductTag, blank=True)
	name = models.CharField(max_length=32)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	slug = models.SlugField(max_length=48)
	active = models.BooleanField(default=True)
	in_stock = models.BooleanField(default=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name 


class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='product-images')
	thumbnail = models.ImageField(upload_to='product-thumbnails', null=True)


class UserManager(BaseUserManager):
	user_in_migrations = True 

	def _create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError('The given email must be set')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user 

	def create_user(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')
		return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
	username = None
	email = models.EmailField('email address', unique=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()


