from django.urls import path

from . import views
from .views import CreatListingView, detailView, watchlistView, addToWatchlist, removeFromWatchList, close_listing


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", CreatListingView, name="create"),
    path("detail/<int:id>", detailView, name="detail"),
    path("watchlist", watchlistView, name="watchlist"),
    path("addToWatchlist/<int:id>", addToWatchlist, name="add_To_watchlist"),
    path("removeFromWatchlist/<int:id>", removeFromWatchList, name="remove_from_watchlist"),
    path("closeListing/<int:id>", close_listing, name="close_listing"),
]
