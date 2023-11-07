import requests
from repositories.models import Language, Repository
from apscheduler.schedulers.background import BackgroundScheduler
import time

# Total Number of Repositories to store in database
TOTAL_REPOSITORIES = 500

# Access token for GitHub API authorization
ACCESS_TOKEN = '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'

# URL for GitHub GraphQL API
API_URL = 'https://api.github.com/graphql'

# Headers for api post request
HEADERS = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
}

# Query for api post request
QUERY = '''
query {
  search(query: "stars:>1000 sort:stars", type: REPOSITORY, first:100 %s) {
    repositories: edges {
      cursor
      info: node {
        ... on Repository {
          name
          description
          url
          language: primaryLanguage {
            name
          }
          stars: stargazerCount
          issues(states: OPEN) {
            count: totalCount
          }
          forks: forkCount
          last_commit: pushedAt
        }
      }
    }
  }
}
'''


def get_repositories(total):
    '''
    Get a list of repositories in JSON format from the GitHub
    GraphQL API. The maximum number of repositories for a single request
    is 100, so this function calls the API multiple times until the
    desired total is reached.

    Keyword Arguments:
    total -- The total number of repositories to retrieve (Should be a multiple of 100)
    '''
    repositories = []
    cursor = ''

    for i in range(total // 100):
        response = requests.post(API_URL,
                                 json={'query': QUERY % cursor},
                                 headers=HEADERS)
        results = response.json().get('data').get('search').get('repositories')
        cursor = f'after: \"{results[-1].get("cursor")}\"'
        repositories.extend(results)

        # Avoid getting rate limited
        time.sleep(3)

    return repositories


def update():
    '''
    Parse data from a list of repositories in JSON format and add the data
    to the database. If the repository already existts, the data for it will
    be updated. If it doesn't exist, a new one will be created.
    '''
    repositories = get_repositories(TOTAL_REPOSITORIES)

    for repository in repositories:

        # Get repository information
        info = repository['info']
        name = info['name']
        description = info['description']
        url = info['url']
        language = info['language']['name'] if info['language'] else 'No Language'
        stars = info['stars']
        issues = info['issues']['count']
        forks = info['forks']
        last_commit = info['last_commit']

        # Create or Update Language instance in database
        defaults = {'name': language}
        language, created = Language.objects.update_or_create(
            name=language, defaults=defaults)

        # Create or Update Repository instance in database
        defaults = {
            'name': name,
            'description': description,
            'url': url,
            'language': language,
            'stars': stars,
            'issues': issues,
            'forks': forks,
            'last_commit': last_commit
        }
        repository, created = Repository.objects.update_or_create(
            url=url, defaults=defaults)


def start():
    '''
    Schedule task to update repository database every hour
    '''
    scheduler = BackgroundScheduler({'apscheduler.timezone': 'UTC'})
    scheduler.add_job(update, 'interval', hours=1)
    scheduler.start()