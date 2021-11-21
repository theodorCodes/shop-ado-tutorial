# Get the profile in get_object_or_404
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
# Check access with login decorator
from django.contrib.auth.decorators import login_required
# Import the user profile model
from .models import UserProfile
# Import the form function from forms.py
from .forms import UserProfileForm
# Import order from checkout to get order_number
from checkout.models import Order

# Create your views here.


@login_required
def profile(request):
    """ Display the user's profile. """
    # Return the profile to the template
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        # Populate form variable with user's current profile information
        form = UserProfileForm(instance=profile)
    # Return the profile with the order, 
    # instead of adding user profile to context
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    # Return form to the template
    # and return order to the template
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)


# for order history in profile.html
def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a post confirmation for order number { order_number }.'
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
    