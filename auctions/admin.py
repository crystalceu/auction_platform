from django.contrib import admin
from .models import User, Categories, Conditions, AuctionListings, Bids, Comments, Watchlist

# Register your models here.
admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Conditions)
admin.site.register(AuctionListings)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Watchlist)