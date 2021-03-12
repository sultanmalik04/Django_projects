from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta, date

class User(AbstractUser):
    def __str__(self):
        return self.username

class Listing(models.Model):
    categries = [
        ('Home & Kitchen', 'Home & Kitchen'),
        ('Electronics', 'Electronics'),
        ('Books', 'Books'),
        ('Toys', 'Toys'),
        ('Fashion', 'Fashion'),
        ('Antiques', 'Antiques'),
        ('Automobile', 'Automobile')
    ]
    title = models.CharField(max_length=50)

    description = models.CharField(max_length=300)

    base_price = models.IntegerField()

    category = models.CharField(choices=categries, max_length=50)

    image_url = models.URLField(max_length=1000)

    publish_date = models.DateTimeField(auto_now_add=True)

    closing_date = models.DateField(default=(date.today()+timedelta(15)), blank=True, editable=True)

    listed_by = models.ManyToManyField(User, blank=True, related_name="listing")

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Bid(models.Model):
    bid_amount = models.IntegerField()
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")
    
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid")
    
    bid_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.listing.title


class Watchlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    list_id = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return self.list_id.title


class Comments(models.Model):
    comment = models.CharField(max_length=600)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    commented_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username