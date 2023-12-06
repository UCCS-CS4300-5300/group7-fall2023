from django.test import TestCase, Client
from django.urls import reverse
from .models import Repository, Language
from repositories import updater
from model_bakery import baker


class ModelTests(TestCase):

    def setUp(self):
      self.language = baker.make(Language)
      self.repository = baker.make(Repository, language=self.language)

    def test_language_create(self):
      self.assertEqual(Language.objects.count(), 1)

    def test_repository_create(self):
      self.assertEqual(Repository.objects.count(), 1)
      
    def test_language_str(self):
      self.assertEqual(self.language.name, str(self.language))


class ViewTests(TestCase):

  def setUp(self):
    baker.make(Repository, _quantity=10)
    self.client =  Client()

  def test_home(self):
    response = self.client.get(reverse('home'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.context['repositories']), 10)

  def test_explore(self):
    response = self.client.get(reverse('explore'))
    self.assertEqual(response.status_code, 200)
  
  def test_account(self):
    response = self.client.get(reverse('account'))
    self.assertRedirects(response, '/login/?next=/account/', status_code=302)
    
class UpdaterTests(TestCase):
    def test_get_repositories(self):
        total = 100
        repositories = updater.get_repositories(total)
        self.assertEqual(len(repositories), total)

    def test_update(self):
      total = 100
      updater.update(total)
      self.assertEqual(Repository.objects.count(), total)
