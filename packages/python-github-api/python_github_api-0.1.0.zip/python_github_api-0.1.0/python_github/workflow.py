from python_github.github_object import GithubObject

class Workflow(GithubObject):
    def __init__(self, token) -> None:
        super().__init__(token)
    def get(self, repository):
        url = self.base_url + "/repos/" + repository + "/actions/workflows"
        return super().request(url)