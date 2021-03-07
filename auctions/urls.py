from django.urls import path

from . import views
from .views import CreatListingView, detailView


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", CreatListingView, name="create"),
    path("detail/<int:id>", detailView, name="detail"),
    path()
]
