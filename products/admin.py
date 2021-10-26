from django.contrib import admin
# Import product model and category
from .models import Product, Category

# Register your models here.


# And then register it with admin.site.register product.
admin.site.register(Product)
# And we might as well import and register the category model here too just in case we need it.
admin.site.register(Category)
