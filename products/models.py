from django.db import models
from django.core.exceptions import ValidationError

from products.fields import LtreeField


class Category(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, related_name='categories', on_delete=models.CASCADE)
    parent_path = LtreeField(db_index=True, editable=False)
    name = models.CharField(max_length=30)
    active = models.BooleanField(default=True)

    def clean(self):
        root_exists = Category.objects.filter(path__root=True).exists()
        is_root = not self.parent
        if is_root and root_exists:
            raise ValidationError('Root already exists.')

    def save(self, *args, **kwargs):
        parent_path = ''
        if self.parent:
            if self.parent.parent_path:
                parent_path = self.parent.parent_path + '.' + str(self.parent.pk)
            else:
                parent_path = str(self.parent.pk)
        self.parent_path = parent_path
        super().save(*args, **kwargs)

    def __str__(self):
        path = self.parent_path + '.' + str(self.pk) if self.parent_path else str(self.pk)
        return '%s - %s' % (self.name, path)


class Product(models.Model):
    parent = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    parent_path = LtreeField(db_index=True, editable=False)
    name = models.CharField(max_length=30)
    active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.parent_path = self.parent.parent_path + '.' + str(self.parent.pk)
        super().save(*args, **kwargs)

    def __str__(self):
        return '%s - %s' % (self.name, self.parent_path + '.' + str(self.pk))
