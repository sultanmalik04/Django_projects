from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Watchlist


def index(request):
    obj = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": obj,
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

# edited code
@login_required(login_url='login')
def CreatListingView(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        base_price = request.POST["base_price"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]

        obj = Listing(title=title, description=description,
                      base_price=base_price, image_url=image_url, category=category)
        obj.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")
# created models --> listings
# Designed form --> createListing
# stop here, to learn BOOTSTRAPE for styling

# deatail view of specified product
def detailView(request, id):
    obj = Listing.objects.get(id=id)
    watchlist_obj = Watchlist.objects.filter(list_id=id)
    return render(request, "auctions/product.html", {
        "product": obj,
        "watchlist_object": watchlist_obj
    })

# Add list to watchlist
def addToWatchlist(request, id):
    current_user_id = request.user.id
    userId = User.objects.get(id = current_user_id)
    listingId = Listing.objects.get(id = id)
    obj = Watchlist()
    obj.user_id = userId
    obj.list_id = listingId
    obj.save()
    return HttpResponseRedirect(reverse("index"))


# watchlist view
def watchlistView(request):
    obj = Watchlist.objects.filter(user_id=request.user.id)
    return render(request, "auctions/watchlist.html", {
        "watchlist": obj
    })

# function to remove a list from the watchlist
def removeFromWatchList(request, id):
    Watchlist.objects.filter(list_id=id).delete()
    return HttpResponseRedirect(reverse("watchlist"))


