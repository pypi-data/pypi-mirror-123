"""Main module."""
from python_github.workflow import Workflow
from python_github.pull_request import PullRequest
from python_github.issue import Issue
from python_github.license import License
import os


class Github():
    def __init__(self):
        token = os.environ["GITHUB_TOKEN"]
        self.workflow = Workflow(token)
        self.pull_request = PullRequest(token)
        self.issue = Issue(token)
        self.license = License(token)