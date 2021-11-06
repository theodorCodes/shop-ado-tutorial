# a*) I'm using the decimal function since this is a financial transaction and using float
# is susceptible to rounding errors.
# So just in general using decimal is preferred when working with money because it's more accurate.
from decimal import Decimal
from django.conf import settings

def bag_contents(request):

    # First let's create an empty list for the bag items to live in.
    bag_items = []
    # I'll also eventually need the total
    total = 0
    # and the product count when we start adding things to the bag.
    # So I'll initialize those now to zero.
    product_count = 0

    # Now in order to entice customers to purchase more.
    # We're going to give them free delivery if they spend more than the amount
    # specified in the free delivery threshold in settings.py.
    # Obviously, there isn't any total yet but once there is I'll just need to
    # check whether it's less than that threshold.
    if total < settings.FREE_DELIVERY_THRESHOLD:
        # If it is less we'll calculate delivery as the total 
        # multiplied by the standard delivery percentage
        # from settings.py. which in this case is 10%.
        # I'm also going to wrap this calculation in the decimal function and import it at
        # the top along with importing our settings file. see top a*): from ... import
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        # For convenience let's also let the user know how much more they need to spend
        # to get free delivery by creating a variable called free_delivery_delta
        # This way we'll be able to entice the user across the site by letting them know
        # they can get free delivery if they just buy a couple more items.
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        # If the total is greater than or equal to the threshold
        # let's set delivery and the free_delivery_delta to zero.
        delivery = 0
        free_delivery_delta = 0
    
    # Finally to calculate the grand total. All I need to do is add the delivery charge to the total.
    grand_total = delivery + total
    
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context