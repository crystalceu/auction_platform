from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("createListing", views.createListing, name="createListing"),
    path("myListings", views.myListings, name="myListings"),
    path("category/<str:category>", views.category, name="category"),
    path("listing/<str:listing>", views.listing, name="listing"),
    path("addWatchlisting", views.addWatchlisting, name="addWatchlisting"),
    path("addComment", views.addComment, name="addComment"),
    path("closeAuction", views.closeAuction, name="closeAuction")
]