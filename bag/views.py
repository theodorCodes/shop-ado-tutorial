from django.shortcuts import render, redirect

# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

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
            else:
                # 5) and otherwise just set it equal to the quantity.
                # Since the item already exists in the bag. But this is a new size for that item.
                bag[item_id]['items_by_size'][size] = quantity
        else:
            # 1) Let's start with the else block. If the items not already in the bag we just need to add it.
            # But we're actually going to do it as a dictionary with a key of items_by_size.
            # Since we may have multiple items with this item id. But different sizes.
            # This allows us to structure the bags such that we can have a single item id for each item.
            # But still track multiple sizes.
            bag[item_id] = {'items_by_size': {size: quantity}}

    # Now I'll wrap the original code in an else block.
    # Such that if there's no size we run this logic.
    # And if there is we'll run the new logic.
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    request.session['bag'] = bag
    return redirect(redirect_url)
    