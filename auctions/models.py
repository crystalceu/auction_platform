from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass

class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length = 64)

class Conditions(models.Model):
    id = models.AutoField(primary_key=True)
    condition_name = models.CharField(max_length = 64)

class AuctionListings(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 48, unique=True)
    description = models.CharField(max_length = 256)
    image = models.CharField(max_length = 256)
    price = models.IntegerField()
    lister = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lister")
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="category")
    condition = models.ForeignKey(Conditions, on_delete=models.CASCADE, related_name="condition")
    time = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=True)

    def category_n(self):
        return self.category.category_name

    def condition_n(self):
        return self.condition.condition_name

    @classmethod
    def create(cls, **dinfo):
        listing = cls(title=dinfo[0], description=dinfo[1], image=dinfo[2], price=dinfo[3], lister=dinfo[4], category=dinfo[5], condition=dinfo[6])
        return listing

class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    item_id = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="item_id")
    user_id = models.ManyToManyField(User, blank=True, related_name="user_id")

    @classmethod
    def create(cls, **dinfo):
        listing = cls(item_id=dinfo[0])
        return listing


class Bids(models.Model):
    id = models.AutoField(primary_key=True)
    bided_item = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="bided_item")
    bider_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bider_id")
    bid = models.IntegerField()
    time = models.DateTimeField(default=timezone.now)

    @classmethod
    def create(cls, **dinfo):
        bid = cls(bided_item=dinfo[0], bider_id=dinfo[1], bid=dinfo[2])
        return bid

class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    com_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="com_user_id")
    com_item_id = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="com_item_id")
    comment = models.CharField(max_length = 256)
    time = models.DateTimeField(default=timezone.now)

    def create(cls, **dinfo):
        comment = cls(com_user_id=dinfo[0], com_item_id=dinfo[1], comment=dinfo[2])
        return comment