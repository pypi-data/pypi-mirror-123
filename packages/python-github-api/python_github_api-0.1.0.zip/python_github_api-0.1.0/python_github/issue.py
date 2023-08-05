from python_github.github_object import GithubObject

class Issue(GithubObject):
    def __init__(self, token) -> None:
        super().__init__(token)
    def get(self, repository, state="open"):
        url = self.base_url + "/repos/" + repository + "/issues"
        if state == "closed":
            url = url + "?&state=closed"
        if state == "open":
            url = url + "?&state=open"
        response = super().request(url)
        ret = []
        for data in response:
            if "pull_request" in data.keys():
                pass
            else:
                ret.append(data)
        return ret