from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from typing import List

from products.models import Category, Product


def get_categories_tree(ordered_categories: List[Category]):
    """
        categories ordered by node count in path in descending order.
    :param ordered_categories:
    :return:
    """
    if not ordered_categories:
        return None
    root = ordered_categories[0]
    root_node = dict(id=root.pk, name=root.name, children=[])
    node_lookup = {root.pk: root_node}

    for category in ordered_categories[1:]:
        parent_pk = category.parent.pk
        if parent_pk in node_lookup:
            node = dict(id=category.pk, name=category.name, children=[])
            node_lookup[parent_pk]['children'].append(node)
            node_lookup[category.pk] = node
    return root_node, node_lookup


def update_with_products(node_lookup: dict, products: List[Product]):
    """
    Update nodes by adding products to categories.
    :param node_lookup:
        categories by their primary key that can be reached from root following active nodes.
    :param products:
    :return:
    """
    for product in products:
        parent_pk = product.parent_category.pk
        if parent_pk in node_lookup:
            node = dict(id=product.pk, name=product.name, price=product.price)
            node_lookup[parent_pk]['children'].append(node)


def get_tree(ordered_categories: List[Category], products: List[Product]):
    """
    :param ordered_categories:
        categories ordered by node count in path in descending order.
    :param products:
    :return:
    """
    tree, lookup = get_categories_tree(ordered_categories)
    update_with_products(lookup, products)
    return tree


class MenuTreeView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        categories = Category.objects.filter(active=True).order_by('path')
        products = Product.objects.filter(active=True)
        tree = get_tree(categories, products)
        return Response(data=tree)
