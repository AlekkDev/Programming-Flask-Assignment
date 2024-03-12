from typing import List

from flask_restx import Model

from .issue import Issue


class Newspaper(object):

    def __init__(self, paper_id: int, name: str, frequency: int, price: float):
        self.paper_id: int = paper_id
        self.name: str = name
        self.frequency: int = frequency  # the issue frequency (in days)
        self.price: float = price  # the monthly price
        self.issues: List[Issue] = []
    def get_issues(self):
        return self.issues
    def add_issue(self, issue: Issue):
        self.issues.append(issue)