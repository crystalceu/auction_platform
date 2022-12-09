from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.db.models import Subquery

from .models import User, Categories, Conditions, AuctionListings, Bids, Comments, Watchlist


def index(request):
    listings = AuctionListings.objects.filter(status=True)
    for listing in listings:
        try:
            listing.price = Bids.objects.filter(bided_item=listing).last().bid
        except:
            listing.price = listing.price
    return render(request, "auctions/index.html", {
        "category": "Active Listings",
        "listings": listings
    })

def listing(request, listing):
    listingQuery = AuctionListings.objects.get(title=listing)
    if request.method == "POST":
        newObject = {'bided_item':listingQuery, 'bider_id':request.user, 'bid':request.POST['bid']}
        bid = Bids.objects.create(**newObject)
        bid.save()
        return HttpResponseRedirect(reverse("listing", kwargs={'listing': listing}))

    else:
        status="Current bid is not your's."
        try:
            bidsQuery = Bids.objects.filter(bided_item=listingQuery)
            numberOfBids, listingQuery.price, listingQuery.bid_owner = len(bidsQuery), bidsQuery.last().bid, bidsQuery.last().bider_id
            if listingQuery.bid_owner == request.user:
                status="Your bid is the current bid."
        except:
            numberOfBids = 0

        try:
            watchlist = Watchlist.objects.filter(user_id=request.user, item_id=listingQuery)
        except:
            watchlist = []
        button_status="btn-secondary" if len(watchlist) == 0 else "btnsuccess"

        commentlist = Comments.objects.filter(com_item_id=listingQuery)

        return render(request, "auctions/listing.html", {
            "listings": listingQuery,
            "bid_status": status,
            "bids": numberOfBids,
            "button_status": button_status,
            "comments": commentlist
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def myListings(request):
    activeListings = AuctionListings.objects.filter(lister=request.user, status=True)
    for listing in activeListings:
        listing.price = Bids.objects.filter(bided_item=listing).last().bid

    archivedListings = AuctionListings.objects.filter(lister=request.user, status=False)
    for listing in archivedListings:
        listing.price = Bids.objects.filter(bided_item=listing).last().bid
        listing.close_time = Bids.objects.filter(bided_item=listing).last().time
    
    closedListings = AuctionListings.objects.filter(status=False)
    wonStatus = False
    for listing in closedListings:
        listing.price = Bids.objects.filter(bided_item=listing).last().bid
        listing.win_time = Bids.objects.filter(bided_item=listing).last().time
        listing.winner = Bids.objects.filter(bided_item=listing).last().bider_id
        if listing.winner == request.user:
            wonStatus = True

    return render(request, "auctions/index.html", {
        "category": "My Listings",
        "listings": activeListings,
        "archivedListings": archivedListings,
        "wonListings": closedListings,
        "wonOrNot": wonStatus
    })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def createListing(request):
    if request.method == "POST":
        # There is no any data falidation, should be added lately
        newObject = {}
        newObject = {'title':request.POST['title'], 'description':request.POST['description'], 
        'image':request.POST['image'],'price':request.POST['price'], 'lister':request.user,
        'category':Categories.objects.get(pk=request.POST['category']), 'condition':Conditions.objects.get(pk=request.POST['condition'])}
        
        try:
            listing = AuctionListings.objects.create(**newObject)
            listing.save()
        except:
            print("Name already exists")
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/createListing.html", {
        "categories": Categories.objects.all(),
        "conditions": Conditions.objects.all()
    })


def watchlist(request):
    activeListings = Watchlist.objects.filter(user_id=request.user, item_id__status=True)
    archivedListings = Watchlist.objects.filter(user_id=request.user, item_id__status=False)
    for listing in activeListings:
        listing.title=listing.item_id.title
        listing.description=listing.item_id.description
        listing.image=listing.item_id.image
        listing.time=listing.item_id.time
        listing.status=AuctionListings.objects.get(title=listing.title).status
        try:
            listing.price = Bids.objects.filter(bided_item=listing.item_id).last().bid
        except:
            listing.price = listing.item_id.price

    for listing in archivedListings:
        listing.title=listing.item_id.title
        listing.description=listing.item_id.description
        listing.image=listing.item_id.image
        listing.time=listing.item_id.time
        listing.close_time=listing.item_id.time
        listing.status=AuctionListings.objects.get(title=listing.title).status
        try:
            listing.price = Bids.objects.filter(bided_item=listing.item_id).last().bid
        except:
            listing.price = listing.item_id.price

    return render(request, "auctions/index.html", {
        "category": "Watchlist",
        "listings": activeListings,
        "archivedListings": archivedListings
    })

def addWatchlisting(request):
    if request.method == "POST":
        watchlist = Watchlist.objects.filter(user_id=request.user, item_id=AuctionListings.objects.get(pk=request.POST['item']))
        watchlist_adduser = Watchlist.objects.filter(item_id=AuctionListings.objects.get(pk=request.POST['item']))
        if len(watchlist) == 0 and len(watchlist_adduser) == 0:
            watchlisting = {'item_id':AuctionListings.objects.get(pk=request.POST['item'])}

            listing = Watchlist.objects.create(**watchlisting)
            listing.save()

            listing = Watchlist.objects.get(item_id=request.POST['item'])
            listing.user_id.add(request.user)

        elif len(watchlist) == 0 and len(watchlist_adduser) != 0:
            listing = Watchlist.objects.get(item_id=request.POST['item'])
            listing.user_id.add(request.user)

        else:
            listing = Watchlist.objects.get(item_id=request.POST['item'])
            listing.user_id.remove(request.user)

        return HttpResponseRedirect(reverse("listing", kwargs={'listing': AuctionListings.objects.get(pk=request.POST['item']).title}))

def addComment(request):
    if request.method == "POST":
        comment = {'com_user_id':request.user, 'com_item_id':AuctionListings.objects.get(pk=request.POST['item']), 'comment':request.POST['comment']}
        listing = Comments.objects.create(**comment)
        listing.save()
    return HttpResponseRedirect(reverse("listing", kwargs={'listing': AuctionListings.objects.get(pk=request.POST['item']).title}))

def closeAuction(request):
    if request.method == "POST":
        listing = AuctionListings.objects.get(pk=request.POST['item'])
        listing.status = False
        listing.save()    
    return HttpResponseRedirect(reverse('index'))

def categories(request):
    categories = Categories.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category):
    category_instance = Categories.objects.get(category_name=category)
    activeListings = AuctionListings.objects.filter(category=category_instance.id)
    for listing in activeListings:
        try:
            listing.price = Bids.objects.filter(bided_item=listing).last().bid
        except:
            listing.price = listing.price
    
    return render(request, "auctions/index.html", {
        "category": category_instance.category_name,
        "listings": activeListings
    })