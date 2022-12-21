from github import Github
import argparse


class Gitcall():

    def __init__(self, access_token):
        self.g = Github(access_token)
        self.repo = self.g.get_repo("Bharat12321/CTFd")

    def get_commits(self):
        commit_counter = 0
        commits = self.repo.get_commits()
        for i in commits:
            commit_counter += 1
        return commit_counter

    def get_pulls(self):
        counter = 0
        open_issues = self.repo.get_issues(state='open')
        for issue in open_issues:
            counter += 1
        return counter

    def get_contributers(self, count=False):
        contributer_list = []
        contributers = self.repo.get_contributors()
        for ctr in contributers:
            contributer_list.append({'contributer-id': ctr.id, 'contributer-title': ctr.name})
        if count:
            return len(contributer_list)
        return contributer_list

    def get_forks(self):
        forks = self.repo.get_forks()
        fork_count = 0
        for i in forks:
            fork_count += 1
        return fork_count

    def get_stars(self):
        return self.repo.stargazers_count

    def get_releases(self):
        releases = self.repo.get_releases()
        release_list = []
        latest_three_release = 0
        for release in releases:
            if latest_three_release >= 3:
                return release_list
            release_list.append({'release-id': release.id, 'release-title': release.title})
            latest_three_release += 1
        return release_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("access_token")
    args = parser.parse_args()
    try:
        obj = Gitcall(args.access_token)
        pull_count = obj.get_pulls()
        print("Pull requests count: ", pull_count)
        fork_count = obj.get_forks()
        print("Forks count : ", fork_count)
        star_count = obj.get_stars()
        print("Stars count : ", star_count)
        releases_lt = obj.get_releases()
        print("Latest three releases : ", releases_lt)
        contributer_count = obj.get_contributers(count=True)
        print("Contributer count: ", contributer_count)
        commit_count = obj.get_commits()
        print("Commits count: ", commit_count)
        contributer_list_desc = obj.get_contributers()
        print("Contributer list desc order: ", contributer_list_desc)
    except Exception as err:
        print("Exception : ", str(err))


main()
