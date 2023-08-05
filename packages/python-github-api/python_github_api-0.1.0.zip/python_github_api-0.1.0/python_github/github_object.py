import requests
from abc import ABCMeta, abstractmethod

class GithubObject(metaclass=ABCMeta):
    token = ""
    base_url = 'https://api.github.com'
    @abstractmethod
    def __init__(self, token) -> None:
        self.token = token
    def request(self, url):
        headers = {'Authorization': 'token ' + self.token}
        response = requests.get(url, headers=headers)
        return response.json()