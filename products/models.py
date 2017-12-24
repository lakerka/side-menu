from django.db import models

from products.fields import LtreeField


class Category(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, related_name='categories', on_delete=models.CASCADE)
    path = LtreeField(db_index=True, editable=False)
    name = models.CharField(max_length=30)
    active = models.BooleanField(default=True)

# TODO prevent saving multiple roots

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.path = self.parent.path + '.' + str(self.pk) if self.parent else self.pk
        super().save(*args, **kwargs)

    def __str__(self):
        return '%s %s' % (self.name, self.path)


class Product(models.Model):
    parent_category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    path = LtreeField(db_index=True, editable=False)
    name = models.CharField(max_length=30)
    active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.path = self.parent_category.path + '.' + str(self.pk)
        super().save(*args, **kwargs)

    def __str__(self):
        return '%s, %s' % (self.name, self.path)
