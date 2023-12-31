import csv
import os
import subprocess
import sys

from dotenv import load_dotenv
import requests

load_dotenv(verbose=True)

WORK_DIR = 'work'
CUR_DIR = os.getcwd()


def github(suffix):
    # github_org = 'toyorepo-github'
    github_org = 'toyorepo-github2'
    endpoint = 'https://api.github.com/user/repos'
    token = os.getenv(f'GITHUB_TOKEN{suffix}')
    headers = {
        'Authorization': f'token {token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    response = requests.get(endpoint, headers=headers)

    if response.status_code != 200:
        return

    for x in response.json():
        name = x['name']
        description = x['description']
        url = x['ssh_url']
        visibility = x['visibility']
        output(url, description, url, description, visibility)


def gitlab(page=100):
    github_org = 'toyorepo-gitlab'
    token = os.getenv('GITLAB_TOKEN')
    headers = {'PRIVATE-TOKEN': token}
    group_id = os.getenv('GITLAB_GROUP_ID')
    endpoint = 'https://gitlab.com/api/v4/'
    endpoint = f'https://gitlab.com/api/v4/groups/{group_id}/projects?per_page={page}'

    response = requests.get(endpoint, headers=headers)

    if response.status_code != 200:
        return

    for x in response.json():
        name = x['name']
        description = x['description']
        url = x['ssh_url_to_repo']
        visibility = x['visibility']
        output(url, name, visibility, description, github_org)


def bitbucket(pagelen=100):
    github_org = 'toyorepo-bitbucket'

    username = os.getenv('BITBUCKET_USERNAME')
    password = os.getenv('BITBUCKET_PASSWORD')
    endpoint = os.getenv('BITBUCKET_ENDPOINT')
    base_url = 'https://bitbucket.org/'

    session = requests.Session()
    session.auth = (username, password)
    params = {'page': 1, 'pagelen': pagelen}
    resp = session.get(endpoint, params=params)
    raw = resp.json()
    values = raw['values']

    for x in values:
        name = x['name']
        description = x['description']
        visibility = 'private' if x['is_private'] else 'public'
        url = x['links']['clone'][1]['href']
        output(url, name, visibility, description, github_org)


def output(url, name, visibility, description, github_org):
    print(f'git clone --bare {url} {WORK_DIR}/{name}')
    print(f'cd {WORK_DIR}/{name}')
    print(f'gh repo create {github_org}/{name} --{visibility} --description="{description}"')
    print(f'git push --mirror git@github.com:{github_org}/{name}')
    print(f'cd {CUR_DIR}')


def usage():
    message = '''\
Usage: main.py [option] - Get repositories

  github toyoake         get gibhub/toyoakekaki
  github jpec            get gibhub/jpec-website
  gitlab                 get gitlab/toyoakekaki
  bitbuckt               get bitbucket/toyoakekaki
'''
    print(message)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    elif sys.argv[1] == 'github':
        if len(sys.argv) != 3:
            usage()
        elif sys.argv[2] == 'toyoake':
            github(suffix='_TOYOAKE')
        elif sys.argv[2] == 'jpec':
            github(suffix='_JPEC')
        else:
            usage()
    elif sys.argv[1] == 'gitlab':
        gitlab()
    elif sys.argv[1] == 'bitbucket':
        bitbucket()
    else:
        usage()
