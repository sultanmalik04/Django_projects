from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Watchlist, Comments, Bid


def index(request):
    obj = Listing.objects.filter(is_active=1)
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

        obj = Listing(title=title, description=description, base_price=base_price, image_url=image_url, category=category)
        obj.save()
        obj.listed_by.add(request.user.id)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")        
# created models --> listings
# Designed form --> createListing
# stop here, to learn BOOTSTRAPE for styling



# deatail view of specified product
# latest: added comment functionality, only logged in user can comment
def detailView(request, id, *argv):
    if request.method == "POST":
        if request.user.is_authenticated:
            comment = request.POST["comment"]
            list_obj = Listing.objects.get(id=id)
            comment_obj = Comments(comment=comment, user=request.user, listing=list_obj)
            comment_obj.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        comment_obj = Comments.objects.filter(listing=id)
        obj = Listing.objects.get(id=id)
        if request.user.is_authenticated:
            watchlist_obj = Watchlist.objects.filter(list_id=id, user_id=request.user.id)
            return render(request, "auctions/product.html", {
                "product": obj,
                "watchlist_object": watchlist_obj,
                "comments": comment_obj,
                "is_owner": obj.listed_by.all()[0] == request.user
            })
        else: 
            return render(request, "auctions/product.html", {
                "product": obj,
                "comments": comment_obj,
                "message": "".join([arg for arg in argv])
            })
            


# Add list to watchlist
@login_required(login_url='login')
def addToWatchlist(request, id):
    current_user_id = request.user.id
    userId = User.objects.get(id = current_user_id)
    listingId = Listing.objects.get(id = id)
    obj = Watchlist()
    obj.user_id = userId
    obj.list_id = listingId
    obj.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# watchlist view
@login_required(login_url='login')
def watchlistView(request):
    obj = Watchlist.objects.filter(user_id=request.user.id)
    return render(request, "auctions/watchlist.html", {
        "watchlist": obj
    })


# function to remove a list from the watchlist
@login_required(login_url='login')
def removeFromWatchList(request, id):
    Watchlist.objects.filter(list_id=id, user_id=request.user.id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def close_listing(request, id):
    return HttpResponse(f"<h1>Close Listing {id}</h1>")


def placeBid(request, id):
    bid= request.POST["bid"]
    list_obj = Listing.objects.get(id=id)
    bid_obj = Bid(bid_amount=bid, user=request.user, listing=list_obj)
    bid_obj.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
