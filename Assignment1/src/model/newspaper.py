from typing import List
import math
from flask_restx import Model

from .issue import Issue


class Newspaper(object):

    def __init__(self, paper_id: int, name: str, frequency: int, price: float):
        self.paper_id: int = paper_id
        self.name: str = name
        self.frequency: int = frequency  # the issue frequency (in days)
        self.price: float = price  # the monthly price
        self.issues: List[Issue] = []
    def get_issue_by_id(self, issue_id: int) -> Issue:
        for issue in self.issues:
            if issue.issue_id == issue_id:
                return issue
            else:
                return ValueError(f"An issue with ID {issue_id} does not exist")
    def get_price_info(self):
        price = self.price
        monthly_freq = math.floor(30/self.frequency)
        monthly_price = price * monthly_freq
        annual_freq = math.floor(365/self.frequency)
        annual_price = price * annual_freq
        print(monthly_freq, annual_freq)
        return monthly_price, annual_price
    def get_issues(self):
        return self.issues
    def add_issue(self, issue: Issue):
        self.issues.append(issue)
    def get_editor_of_issue(self, issue_id: int):
        issue = self.get_issue_by_id(issue_id)
        return issue.editor_id
    def delete_issues(self):
        self.issues = []