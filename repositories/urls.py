from django.urls import path
from .views import AccountPageView, ExplorePageView,login,logout,signup,CreateProfile, home

urlpatterns = [
  path('login/', login, name='login'),
  path('logout/',logout,name='logout'),
  path('signup/',signup,name='signup'),
  path('create-profile/', CreateProfile.as_view(), name='create_profile'),
  path("", home, name="home"),
  path("account/", AccountPageView.as_view(), name="account"),
  path("explore/", ExplorePageView.as_view(), name="explore"),
]