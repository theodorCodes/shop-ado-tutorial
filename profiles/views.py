# Get the profile in get_object_or_404
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

# Import the user profile model
from .models import UserProfile
# Import the form function from forms.py
from .forms import UserProfileForm


# Create your views here.


def profile(request):
    """ Display the user's profile. """
    # Return the profile to the template
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')

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