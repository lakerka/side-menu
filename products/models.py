from django.db import models

from products.fields import LtreeField


class Product(models.Model):
    path = LtreeField(db_index=True)
    name = models.CharField(max_length=30)
    active = models.BooleanField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Category(models.Model):
    path = LtreeField(db_index=True)
    name = models.CharField(max_length=30)
    active = models.BooleanField()
