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

    def get_forks(self):
        forks = self.repo.get_forks()
        for i in forks:
            print('frk: ', i)
        return 0

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
        commit_count = obj.get_commits()
        pull_count = obj.get_pulls()
        fork_count = obj.get_forks()
        star_count = obj.get_stars()
        releases_lt = obj.get_releases()        

        print("commit_count: ", commit_count)
        print("pull_count: ", pull_count)
        print("fork_count: ", fork_count)
        print("star_count: ", star_count)
        print("releases_lt: ", releases_lt)

    except Exception as err:
        print("Exception : ", str(err))


main()
