from django.shortcuts import render
# For now let's import the product model.
from .models import Product


# And just change the name from index to all_products.


def all_products(request):
    # This view is going to show all products
    # but eventually will also handle sorting in searches too
    # so I'll add that to the docstring.
    """ A view to show all products, including sorting and search queries """

    # And just return all products from the database using product.objects.all
    products = Product.objects.all()

    # I'll add that to the context so our products will be available in the template.
    context = {
        'products': products,
    }

    # It's going to return products/products.html which we'll build in a moment.
    # And it will also need a context since we'll need to send some things back to the template.
    return render(request, 'products/products.html', context)
