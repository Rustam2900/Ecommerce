from django.db import models

from base.models import TimeStampModel
from categories.models import Category


class Discount(TimeStampModel):
    dis_percentage = models.IntegerField(blank=True, null=True)
    end_time = models.DateTimeField()

    def __str__(self):
        return str(self.dis_percentage)


class Product(TimeStampModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f"{self.id} {self.slug}"


class Color(TimeStampModel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='color')
    color = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.slug


class Size(TimeStampModel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='size')
    size = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.slug


class Images(TimeStampModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    images = models.ImageField(upload_to='product/images')

    def __str__(self):
        return self.product.name


class Stars(TimeStampModel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stars')
    stars = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.product.name
