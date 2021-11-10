from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
# Required for Bootstrap toast messages
from django.contrib import messages
from products.models import Product

# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    # product = Product.objects.get(pk=item_id)
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        # 2) If the item is already in the bag.
        if item_id in list(bag.keys()):
            # 3) Then we need to check if another item of the same id and same size already exists.
            if size in bag[item_id]['items_by_size'].keys():
                # 4) And if so increment the quantity for that size 
                bag[item_id]['items_by_size'][size] += quantity
                # response message
                messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
            else:
                # 5) and otherwise just set it equal to the quantity.
                # Since the item already exists in the bag. But this is a new size for that item.
                bag[item_id]['items_by_size'][size] = quantity
                # response message
                messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
        else:
            # 1) Let's start with the else block. If the items not already in the bag we just need to add it.
            # But we're actually going to do it as a dictionary with a key of items_by_size.
            # Since we may have multiple items with this item id. But different sizes.
            # This allows us to structure the bags such that we can have a single item id for each item.
            # But still track multiple sizes.
            bag[item_id] = {'items_by_size': {size: quantity}}
            # response message
            messages.success(request, f'Added size {size.upper()} {product.name} to your bag')

    # Now I'll wrap the original code in an else block.
    # Such that if there's no size we run this logic.
    # And if there is we'll run the new logic.
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            # response message
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag[item_id] = quantity
            # response message
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


# Adjust bag items
# It still takes the request and item id as parameters.
def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified product to the shopping amount """

    product = get_object_or_404(Product, pk=item_id)
    # And the entire top portion
    # will be the same except we don't need the redirect URL since we'll always want
    # to redirect back to the shopping bag page.
    quantity = int(request.POST.get('quantity'))
    # redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        # Remember that this is coming from a form on the shopping bag page which will
        # contain the new quantity the user wants in the bag. 
        # So the basic idea here is that if quantity is greater than zero 
        if quantity > 0:
            # we'll want to set the items quantity accordingly 
            bag[item_id]['items_by_size'][size] = quantity
            # response message
            messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
        else:
            # and otherwise we'll just remove the item.
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            # response message
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')

    # Summary to aboves if statement:        
    # If there's a size. Of course we'll need to drill into the
    # items by size dictionary, find that specific size and either set its
    # quantity to the updated one or remove it if the quantity submitted is zero.

    # Summary to below else statement:
    # If there's no size that logic is quite simple and we can remove the item
    # entirely by using the pop function.
    else:
        if quantity > 0:
            bag[item_id] = quantity
            # response message
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag.pop(item_id)
            # response message
            messages.success(request, f'Removed {product.name} from your bag')
    # These two operations are basically the same.
    # They just need to be handled differently due to the more complex structure of the
    # bag for items that have sizes.

    request.session['bag'] = bag
    # With that finished we just need to redirect back
    # to the view bag URL. And I'll use the reverse function to do that.
    # Importing it here at the top, see TOP
    return redirect(reverse('view_bag'))


# Remove bag item
# change name to remove_from_bag()
def remove_from_bag(request, item_id):
    """ Remove the item from the shopping bag """

    try:
        # adding product here
        product = get_object_or_404(Product, pk=item_id)
        # We don't need the quantity in this view since the intended quantity is zero.
        ## quantity = int(request.POST.get('quantity'))
        # Now if the user is removing a product with sizes.
        # We want to remove only the specific size they requested.
        # So if size is in request.post, such as in *a) and in *b)
        # We'll want to delete that size key in the items by size dictionary at *c).
        size = None
        if 'product_size' in request.POST:
            # v-- *a)
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        #  v-- *b)
        if size:
            #                                 v-- *c)
            del bag[item_id]['items_by_size'][size]
            # Also if that's the only size they had in the bag.
            # In other words, if the items by size dictionary is now empty which will evaluate to false.
            if not bag[item_id]['items_by_size']:
                # We might as well remove the entire item id so we don't end up with an empty items
                # by size dictionary hanging around.
                bag.pop(item_id)
                # We should also do this in the adjust bag view if the quantity is set to zero.
                # See *d)
            # response message
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
        else:
            # If there is no size. Again removing the item is as simple as popping it out of the bag.
            bag.pop(item_id)  ## TYPO HERE! change from: [item_id] to: (item_id) 
            # response message
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        # Finally instead of returning a redirect.
        ## return redirect(reverse('view_bag'))
        # Because this view will be posted to from a JavaScript function.
        # We want to return an actual 200 HTTP response.
        # Implying that the item was successfully removed.
        return HttpResponse(status=200)
    except Exception as e:
        # response message
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)