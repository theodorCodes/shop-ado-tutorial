from django.db import models

# Create your models here.


# I'll start with the category model which will give our products a category
# like clothing, kitchen and dining, or deals.
# And that'll inherit from models.Model
class Category(models.Model):

    # Fixing names in admin showing Categorys instead of Categories
    class Meta:
        verbose_name_plural = 'Categories'

    # This model is quite simple,
    # all it contains is a name which is a character field that represents the programmatic name
    # And we'll give that a max length of 254
    name = models.CharField(max_length=254)
    # And a friendly name which will make that name a little bit more friendly looking for the front end.
    # And this will also have a max length of 254
    # And we'll make it null equals true and blank equals true so that the friendly name is optional.
    # If you look at bed and bath in the categories fixture for example
    # you'll see the friendly name is a bit nicer, but the name field gives us a
    # programmatic way to find it in things like views and other code.
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    # We'll also create a string method here.
    # Which takes in the category model itself.
    # And just returns self.name
    def __str__(self):
        return self.name

    # I'm also going to make a quick model method here which is the same thing as the string method
    # except this one is going to return the friendly name if we want it.
    # so return self.friendly_name.
    def get_friendly_name(self):
        return self.friendly_name


# The product model isn't much more complex other than just having a few more fields.
# The first field is a foreign key to the category model.
# We'll allow this to be null in the database and blank in forms
# and if a category is deleted we'll set any products that use it to have null for this field
# rather than deleting the product.
class Product(models.Model):
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    # The rest of the fields are pretty straightforward so let's paste those in from the completed project.
    # Each product has a SKU, a name, and a description.
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    # And it's also got a couple of decimal fields for price and rating.
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    # And an image url and an image field.
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    # As usual, the string method will just return the products name
    # so I'll copy that from the category model.
    # And it's worth noting what we're requiring here
    # each product requires a name, a description, and a price.
    # But everything else is optional.
    def __str__(self):
        return self.name  # self.name REFERS TO THE NAME ABOVE!
