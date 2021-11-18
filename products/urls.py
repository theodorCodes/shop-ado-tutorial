# And this is a good reminder it actually looks like we aren't even
# using the admin from django.contrib in either of these files.
# So I'm going to remove it from both just to make sure that our code stays clean
# It probably came in when we copied the project-level file to create this originally.
# --> from django.contrib import admin <--
from django.urls import path
from . import views

urlpatterns = [
    # But, any way to finish this file.
    # All we have to do is change the view from index to all_products.
    # And the name from 'home' to 'products'.
    path('', views.all_products, name='products'),
    # which will contain the product Id
    # and that will return the product detail  view and be named product detail.
    # Added int: and trailing slash / to wrap 'product_id'
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    # Add product page
    path('add/', views.add_product, name='add_product'),
    # Edit product page
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
]
