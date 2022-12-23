import json
import re
import requests
import argparse
from requests.auth import HTTPBasicAuth


class Gitcall():

    def __init__(self, access_token, username, repo):
        self.username = username
        self.repo = repo
        self.authentication = HTTPBasicAuth(self.username, access_token)
        self.git_api_base_url = 'https://api.github.com'

    def get_basic_info(self):
        url = '{git_api_base_url}/repos/{username}/{repo}?page=$i&per_page=100'.format(
            git_api_base_url=self.git_api_base_url,
            username=self.username, 
            repo=self.repo
        )
        res = requests.get(url, auth = self.authentication)
        try:
            res = res.json()
        except Exception as err:
            print("Error in get_basic_info: ", err)
            res = dict()
        return res

    def get_commits_count(self):
        url = '{git_api_base_url}/repos/{username}/{repo}/commits?per_page=1'.format(
            git_api_base_url=self.git_api_base_url,
            username=self.username, 
            repo=self.repo
            )
        try:
            return re.search('\d+$', requests.get(url, auth = self.authentication).links['last']['url']).group()
        except Exception as err:
            print("Error in get_commits_count: ", err)
            return 0 

    def get_contributers(self, count=False):
        contributers_list = []
        contributers_count = 0        
        page = 1
        while True:
            url = '{git_api_base_url}/repos/{username}/{repo}/contributors?page={page}&per_page=100'.format(
                git_api_base_url=self.git_api_base_url,
                username=self.username,
                repo=self.repo,
                page=page)
            try:
                res = requests.get(url, auth = self.authentication)
            except Exception as err:
                return err
            res_json = res.json()
            for data in res_json:
                contributers_list.append(data)
            repos_fetched = len(res_json)
            contributers_count = contributers_count + repos_fetched
            if (repos_fetched == 100):
                page = page + 1
            else:
                break
        if count:
            return contributers_count
        return contributers_list

    def get_list_of_contributers_according_to_contributions(self):
        main_list = []
        con_lst = self.get_contributers()
        con_lst = con_lst
        for contributer in con_lst:
            main_list.append(contributer)
        return main_list

    def get_stars_count(self):
        res = self.get_basic_info()
        return res.get('stargazers_count', 0)

    def get_open_issues_count(self):
        res = self.get_basic_info()
        return res.get('open_issues_count', 0)

    def get_forks_count(self):
        res = self.get_basic_info()
        return res.get('forks_count', 0)

    def get_latest_three_releases(self):
        url = '{git_api_base_url}/repos/{username}/{repo}/tags'.format(
            git_api_base_url=self.git_api_base_url,
            username=self.username, 
            repo=self.repo
        )
        try:
            res = requests.get(url, auth = self.authentication)
            res = res.json()
        except Exception as err:
            print("Error in get_latest_three_releases: ", err)
            res =  list()
        return res[0:3]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("access_token")
    username = 'bharat12321'
    repo = "CTFd"
    args = parser.parse_args()

    try:
        obj = Gitcall(args.access_token, username, repo)

        commits_count = obj.get_commits_count()
        print("Commits Count: ", commits_count)

        stars_count = obj.get_stars_count()
        print("Stars Count: ", stars_count)

        open_issues_count = obj.get_open_issues_count()
        print("Open Issues Count: ", open_issues_count)

        forks_count = obj.get_forks_count()
        print("Forks Count: ", forks_count)

        releases_count = obj.get_latest_three_releases()
        print("Latest Three Release: ", releases_count)

        contributers_count = obj.get_contributers(count=True)
        print("Contributers Count: ", contributers_count)

        contributers_list = obj.get_contributers()
        print("Contributers List: ", contributers_list)

        contributers_list_by_contribuution_desc = obj.get_list_of_contributers_according_to_contributions()
        print("Contributers List By Decending no Of Contributions: ", contributers_list_by_contribuution_desc)

    except Exception as err:
        print("Exception : ", str(err))

main()
