import requests
from repositories.models import Language, Repository

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
  search(query: "stars:>1000 sort:stars", type: REPOSITORY, first:2, %s) {
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
    repositories = []
    cursor = ''

    for i in range(total // 2):
        response = requests.post(API_URL,
                                 json={'query': QUERY % cursor},
                                 headers=HEADERS)
        results = response.json().get('data').get('search').get('repositories')
        cursor = f'after: \"{results[-1].get("cursor")}\"'
        repositories.extend(results)

    return repositories


def update_database(repositories):
    for repository in repositories:

        # Get repository information
        info = repository['info']
        name = info['name']
        description = info['description']
        url = info['url']
        language = info['language']['name'] if info['language'] else "None"
        stars = info['stars']
        issues = info['issues']['count']
        forks = info['forks']
        last_commit = info['last_commit']

        # Create or Update Language db instance
        defaults = {'name': language}
        language, created = Language.objects.update_or_create(
            name=language, defaults=defaults)

        # Create or Update Repository db instance
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


repositories = get_repositories(10)
update_database(repositories)
