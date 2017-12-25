from django.contrib import admin

from products.models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        read_only_field = []
        if obj:
            read_only_field = ['parent']
        return read_only_field


class ProductAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        read_only_field = []
        if obj:
            read_only_field = ['parent_category']
        return read_only_field


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
