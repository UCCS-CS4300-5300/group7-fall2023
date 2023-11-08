from django.urls import path
from .views import HomePageView, AccountPageView, ExplorePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("/account", AccountPageView.as_view(), name="account"),
    path("/explore", ExplorePageView.as_view(), name="explore"),
]