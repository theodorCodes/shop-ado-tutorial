from django.contrib import admin
# Import product model and category
from .models import Product, Category

# Register your models here.

# I'll create two classes
# product admin and category admin
# Both of which will extend the built in model admin class.


class ProductAdmin(admin.ModelAdmin):
    # For products let's add the list display attribute.
    # Which is a tuple that will tell the admin which (existing) fields to display.
    # I'll add SKU, name, category, price, rating, and image
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    # Finally, let's sort the products by SKU using the ordering attribute.
    # Since it's possible to sort on multiple columns note that this does
    # have to be a tuple even though it's only one field.
    # To reverse it you can simply stick a minus in front of SKU.
    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    # I'll also add friendly_name and name to the category admin class to make sure
    # that those display there.
    # And by the way, if you want to change the order of the columns in the admin
    # you can just adjust the order here in the list display attribute.
    list_display = (
        'friendly_name',
        'name',
    )


# And then register it with admin.site.register product.
# adding ProductAdmin and CategoryAdmin
admin.site.register(Product, ProductAdmin)
# And we might as well import and register the category model here too just in case we need it.
admin.site.register(Category, CategoryAdmin)
