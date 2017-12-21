from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from products.fields import LtreeField


def validate_id_matches_last_path_element(id, path, prefix):
    current = path.split('.')[-1]
    current_id = current.lstrip(prefix)
    if str(id) != current_id:
        raise ValidationError(_('Last path element id must match item id.'), code='invalid', )


def validate_has_prefix(path, prefix):
    current = path.split('.')[-1]
    if not current.startswith(prefix):
        raise ValidationError(_('Last path element must be prefixed with: %s.' % prefix), code='invalid', )


def validate_has_path(path):
    if not path:
        raise ValidationError(_('Missing path.'), code='required', )


def validate_has_parent(path):
    if '.' not in path:
        raise ValidationError(_('Parent does not exist.'), code='invalid', )


def get_parent_path(path):
    validate_has_parent(path)
    return '.'.join(path.split('.')[:-2])


def get_parent(path):
    validate_has_parent(path)
    parent = path.split('.')[-2]
    return parent


def validate_parent_exists(path):
    """
    Uses implicit assumption that Product cannot have children.
    """
    parent_path = get_parent_path(path)
    has_parent = Category.objects.filter(path=parent_path).exists()
    if not has_parent:
        ValidationError(_('Parent does not exist.'), code='invalid', )


def validate_parent_is_not_product(path):
    parent = get_parent(path)
    parent_is_product = parent.startswith('p')
    if parent_is_product:
        raise ValidationError(_('Parent cannot be product.'), code='invalid', )


def validate_single_root(path):
    """
    Uses implicit assumption that only Category can be root.
    """
    is_root = '.' not in path
    root_exists = Category.objects.filter(path__root=True).exists()
    if is_root and root_exists:
        raise ValidationError(_('Root already exists.'), code='invalid', )


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    path = LtreeField(db_index=True)
    name = models.CharField(max_length=30)
    active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    PREFIX = 'p'

    def clean(self):
        path = self.path
        validate_has_path(path)
        validate_parent_exists(path)
        validate_parent_is_not_product(path)
        validate_has_prefix(path, self.PREFIX)
        validate_id_matches_last_path_element(self.id, path, self.PREFIX)

    def __str__(self):
        return '%s (%s, %s)' % (self.__class__.__name__, self.name, self.path)


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    path = LtreeField(db_index=True)
    name = models.CharField(max_length=30)
    active = models.BooleanField(default=True)

    PREFIX = 'c'

    def clean(self):
        path = self.path
        validate_has_path(path)
        validate_single_root(path)
        is_root = '.' not in path
        if not is_root:
            validate_parent_exists(path)
        validate_has_prefix(path, self.PREFIX)
        validate_id_matches_last_path_element(self.id, path, self.PREFIX)

    def __str__(self):
        return '%s (%s, %s)' % (self.__class__.__name__, self.name, self.path)
