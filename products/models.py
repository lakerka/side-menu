from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from products.fields import LtreeField


def validate_is_not_root(path):
    is_root = '.' not in path
    if is_root:
        raise ValidationError(
            _('Item cannot be root'),
            code='invalid',
        )


def validate_single_root(objects, path):
    is_root = '.' not in path
    root_exists = objects.filter(path__root=True).exists()
    if is_root and root_exists:
        raise ValidationError(
            _('Root already exists'),
            code='invalid',
        )


def validate_has_parent(objects, path):
    is_root = '.' not in path
    # TODO there might be errors
    parent_path = '.'.join(path.split('.')[:-1])
    has_parent = objects.filter(path=parent_path).exists()
    if not (is_root or has_parent):
        raise ValidationError(
            _('Parent does not exist'),
            code='invalid',
        )


def validate_path(objects, path):
    if not path:
        raise ValidationError(
            _('Missing path'),
            code='required',
        )
    validate_single_root(objects, path)
    validate_has_parent(objects, path)


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    path = LtreeField(db_index=True)
    name = models.CharField(max_length=30)
    active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        validate_is_not_root(self.path)
        validate_path(Product.objects, self.path)


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    path = LtreeField(db_index=True)
    name = models.CharField(max_length=30)
    active = models.BooleanField(default=True)

    def clean(self):
        validate_path(Category.objects, self.path)

# TODO investigate postgres GIST index
