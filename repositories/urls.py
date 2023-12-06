from django.urls import path
from .views import AccountPageView,login,logout,signup,CreateProfile, home, explore

urlpatterns = [
  path('login/', login, name='login'),
  path('logout/',logout,name='logout'),
  path('signup/',signup,name='signup'),
  path('create-profile/', CreateProfile.as_view(), name='create_profile'),
  path("", home, name="home"),
  path("account/", AccountPageView.as_view(), name="account"),
  path("explore", explore, name="explore"),
]