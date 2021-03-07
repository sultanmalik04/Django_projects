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

    image_url = models.URLField(max_length=500)

    publish_date = models.DateTimeField(auto_now_add=True)

    closing_date = models.DateField(default=(date.today()+timedelta(15)), blank=True, editable=True)

    owner = models.ManyToManyField(User, blank=True, related_name="listings")

    #status = models.BooleanField(default=True)

    def __str__(self):
        return self.title
