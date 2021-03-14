from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib import messages
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
        watchlist_obj = Watchlist.objects.filter(list_id=id, user_id=request.user.id)
        prev_bids = Bid.objects.filter(listing=obj).order_by("-bid_amount")
        if len(prev_bids) > 0:
            highest_bider = prev_bids[0]
        else:
            highest_bider = None
        return render(request, "auctions/product.html", {
                "product": obj,
                "watchlist_object": watchlist_obj,
                "comments": comment_obj,
                "is_owner": obj.listed_by.all()[0] == request.user,
                "is_active": obj.is_active,
                "prev_bids": prev_bids,
                "highest_bider": highest_bider,
                "current_user": request.user.username,
                "owner": obj.listed_by.all()[0]
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
    list_obj = Listing.objects.get(id=id)
    list_obj.is_active = 0
    list_obj.save()
    messages.add_message(request, messages.SUCCESS, 'Listing closed successfully!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def placeBid(request, id):
    bid= request.POST["bid"]
    list_obj = Listing.objects.get(id=id)
    prev_bids = Bid.objects.filter(listing=list_obj)
    if len(prev_bids) > 0:
        max_prev_bid = prev_bids.order_by("-bid_amount")[0].bid_amount
    else:
        max_prev_bid = 0
    if not list_obj.is_active:
        messages.add_message(request, messages.ERROR, 'sorry! this listing is now closed, You can not place bid on this item.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    elif int(bid) <= int(list_obj.base_price):
        messages.add_message(request, messages.WARNING, 'Your bid should be greater than base price.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    elif int(bid) <= int(max_prev_bid):
        #messages.error(request, 'Your bid is less then the highest bid')
        messages.add_message(request, messages.INFO, 'Your bid is less then the highest bid')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:    
        bid_obj = Bid(bid_amount=bid, user=request.user, listing=list_obj)
        bid_obj.save()
        #messages.success(request, 'congratulations! your bid is recorded.')
        messages.add_message(request, messages.SUCCESS,'congratulations! your bid is recorded.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def categoriesView(request):
    categories = ['Home & Kitchen', 'Electronics', 'Books', 'Toys', 'Fashion', 'Antiques', 'Automobile']
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def categoryView(request, category):
    list_obj = Listing.objects.filter(category=category, is_active=1)
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": list_obj
    })
