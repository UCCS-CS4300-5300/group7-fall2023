from django.views.generic.base import TemplateView
from .models import Repository, Language, UserProfile
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404, reverse
from django.contrib import messages
from .forms import UserUpdateForm, UserProfileUpdateForm, SignupForm, LoginForm,CreateProfileForm, SearchForm
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

def home(request):
  if request.method == 'POST':
    search_form = SearchForm(request.POST)
    if search_form.is_valid():
      query = search_form.cleaned_data['query']
      parameter = f'?query={query}' if query else ''
      return redirect(reverse('explore') + parameter) 
  else:
    search_form = SearchForm()
  context = {
    'repositories': Repository.objects.all().order_by('-stars')[:10],
    'search_form': search_form
  }
  return render(request, 'home.html', context=context)
 
  
def explore(request):
  if request.method == 'POST':
    search_form = SearchForm(request.POST)
    if search_form.is_valid():
      query = search_form.cleaned_data['query']
      parameter = f'?query={query}' if query else ''
      return redirect(reverse('explore') + parameter) 
  else:
    repositories = Repository.objects.all()
    search_form = SearchForm()
    query = request.GET.get('query')
    
    if query:
      repositories = repositories.filter(name__icontains=query)
      
  context = {
    'repositories': repositories.order_by('-stars')[:10],
    'languages': Language.objects.all(),
    'search_form': search_form
  }
  return render(request, 'explore.html', context=context)
    

def login(request):
      if request.method == 'POST':
          form = LoginForm(request.POST)
          if form.is_valid():
              username = form.cleaned_data['username']
              password = form.cleaned_data['password']
              user = authenticate(request, username=username, password=password)
              if user is not None:
                  auth_login(request, user)
                  return redirect('create_profile')
              else:
                  messages.error(request, 'Invalid username or password.')
      else:
          form = LoginForm()
      return render(request, 'login.html', {'form': form})


def signup(request):
      if request.method == 'POST':
          form = SignupForm(request.POST)
          if form.is_valid():
              user = form.save()
              messages.success(
                  request,
                  f'Account created for {user.username}! You can now log in.')
              return redirect('login')
      else:
          form = SignupForm()
      return render(request, 'signup.html', {'form': form})


@login_required
def logout(request):
      auth_logout(request)
      messages.success(request, 'You have been logged out.')
      return redirect('home')


def custom_400_error(request, exception=None):
      return HttpResponseBadRequest(render(request, '400.html'), status=400)


class AccountPageView(LoginRequiredMixin, TemplateView):
      template_name = "account.html"
      login_url = '/login/'

      def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        print(user)
        try:
          user_profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
          # Create a UserProfile if it doesn't exist for the current user
          user_profile = UserProfile.objects.create(user=self.ExplorePageViewrequest.user)
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileUpdateForm(instance=user_profile)
        context['user_form'] = user_form
        context['profile_form'] = profile_form
        return context



      # @login_required
      def get(self, request, *args, **kwargs):
          user = request.user
          user_profile = UserProfile.objects.get(user=user)

          user_form = UserUpdateForm(instance=user)
          profile_form = UserProfileUpdateForm(instance=user_profile)

          context = {
              'user_form': user_form,
              'profile_form': profile_form,
          }
          return render(request, self.template_name, context)

      # @login_required
      def post(self, request, *args, **kwargs):
          user = request.user
          user_profile = UserProfile.objects.get(user=user)

          user_form = UserUpdateForm(request.POST, instance=user)
          profile_form = UserProfileUpdateForm(request.POST,
                                               request.FILES,
                                               instance=user_profile)

          if user_form.is_valid() and profile_form.is_valid():
              user_form.save()
              profile_form.save()
              messages.success(request,
                               'Your profile has been updated successfully.')
              return redirect('account')
          else:
              messages.error(request, 'Please correct the errors below.')

          context = {
              'user_form': user_form,
              'profile_form': profile_form,
               'user': request.user,
          }
          return render(request, self.template_name, context)

      def dispatch(self, *args, **kwargs):
          response = super().dispatch(*args, **kwargs)
          if response.status_code == 400:
              return HttpResponseBadRequest(render(self.request, '400.html'))
          return response

class CreateProfile(View):
      template_name = 'create_profile.html'

      def get(self, request):
          try:
              user_profile = UserProfile.objects.get(user=request.user)
              # If the profile exists, redirect to the home page
              return redirect('home')
          except UserProfile.DoesNotExist:
              form = CreateProfileForm()
              return render(request, self.template_name, {'form': form})

      def post(self, request):
          form = CreateProfileForm(request.POST, request.FILES)
          if form.is_valid():
              profile = form.save(commit=False)
              profile.user = request.user  # Assign the current user to the profile
              profile.save()
              return redirect('home')  # Redirect to home 
          return render(request, self.template_name, {'form': form})