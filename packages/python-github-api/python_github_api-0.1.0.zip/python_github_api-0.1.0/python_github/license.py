from python_github.github_object import GithubObject

class License(GithubObject):
    def __init__(self, token) -> None:
        super().__init__(token)
    def get(self, repository):
        url = self.base_url + "/repos/" + repository + "/license"
        response = super().request(url)
        if "license" in response.keys():
            return response["license"]["name"]
        return None