# Get the profile in get_object_or_404
from django.shortcuts import render, get_object_or_404

# Import the user profile model
from .models import UserProfile


# Create your views here.


def profile(request):
    """ Display the user's profile. """
    # Return the profile to the template
    profile = get_object_or_404(UserProfile, user=request.user)

    template = 'profiles/profile.html'
    # Add user profile to context
    context = {
        'profile': profile,
    }

    return render(request, template, context)