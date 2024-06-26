from django.db import models
from django.contrib.auth.models import User

class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    logo = models.FileField(upload_to="brand/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    icon = models.FileField(upload_to="category/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Smartphone(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.FileField(upload_to="smartphones/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField()
    screen_size = models.CharField(max_length=50)
    battery_capacity = models.CharField(max_length=50)
    ram = models.CharField(max_length=50)
    storage = models.CharField(max_length=50)
    camera_resolution = models.CharField(max_length=50)
    processor = models.CharField(max_length=50)
    totalreview = models.IntegerField(default=1)
    totalrating = models.IntegerField(default=5)

    def __str__(self):
        return self.name

class Review(models.Model):
	customer = models.ForeignKey(User, on_delete=models.CASCADE)
	smartphone = models.ForeignKey(Smartphone, on_delete=models.CASCADE)
	review_star = models.IntegerField()
	review_text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

