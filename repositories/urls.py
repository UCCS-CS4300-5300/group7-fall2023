from django.urls import path
from .views import HomePageView, AccountPageView, ExplorePageView,login,logout,signup,CreateProfile

urlpatterns = [
   path('login/', login, name='login'),
  path('logout/',logout,name='logout'),
  path('signup/',signup,name='signup'),
  path('create-profile/', CreateProfile.as_view(), name='create_profile'),
    path("", HomePageView.as_view(), name="home"),
  path("account/", AccountPageView.as_view(), name="account"),
    path("explore/", ExplorePageView.as_view(), name="explore"),
]