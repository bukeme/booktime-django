from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
from urllib import request 
from main import models 
import requests

endpoint = 'https://fakestoreapi.com/products'

response = requests.get(endpoint)

data = response.json()

for item in data:
	product = models.Product.objects.create(
		name=item['title'],
		description=item['description'],
		price=item['price'],
		slug=slugify(item['title'])
	)
	image_url = item['image']
	image_name = image_url.split('/')[-1]

	image_response = requests.get(image_url, stream=True)
	image_response.raw.decode_content = True
	image_response = image_response.raw
	product_image = models.ProductImage(product=product)
	product_image.image.save(image_name, ContentFile(image_response.read()), save=False)
	product_image.save()

	tag = item['category'].split(' ')[-1]
	# tag_exist = False
	try:
		product_tag = models.ProductTag.objects.get(name=tag)
		product_tag.products.add(product)
		product_tag.save()
		# tag_exist = True
	except:
		product_tag = models.ProductTag.objects.create(
			name=tag,
			slug=tag,
			description=tag
		)
		product_tag.products.add(product)
		product_tag.save()
		# saved_tag = product_tag.save()
		# saved_tag.products.add(product)
		# saved_tag.save()
