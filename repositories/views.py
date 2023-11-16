from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Repository
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["repositories"] = Repository.objects.all().order_by(
            '-stars')[:10]
        return context


class AccountPageView(TemplateView):
    template_name = "account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ExplorePageView(TemplateView):
    template_name = "explore.html"

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["repositories"] = Repository.objects.all()
      return context

def login(request):
  return render(request, 'login.html')

@login_required 
def home(request):
  return render(request, 'home.html')