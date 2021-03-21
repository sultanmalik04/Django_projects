from django.contrib import admin

from .models import User, Listing, Comments, Watchlist, Bid

# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Watchlist)
admin.site.register(Comments)
admin.site.register(Bid)
