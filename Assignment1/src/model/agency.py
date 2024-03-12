from typing import List, Union, Optional

from .newspaper import Newspaper
from .issue import Issue

class Agency(object):
    singleton_instance = None

    def __init__(self):
        self.newspapers: List[Newspaper] = []

    @staticmethod
    def get_instance():
        if Agency.singleton_instance is None:
            Agency.singleton_instance = Agency()

        return Agency.singleton_instance

    def add_newspaper(self, new_paper: Newspaper):
        if self.get_newspaper(new_paper.paper_id) is None:
            self.newspapers.append(new_paper)
        else:
            # IF the condition is False, raise a ValueError
            raise ValueError(f"A newspaper with ID {new_paper.paper_id} already exists")

    def get_newspaper(self, paper_id: Union[int,str]) -> Optional[Newspaper]:
        for paper in self.newspapers:
            if paper.paper_id == paper_id:
                return paper
        return None

    def all_newspapers(self) -> List[Newspaper]:
        return self.newspapers

    def remove_newspaper(self, paper: Newspaper):
        self.newspapers.remove(paper)

    def update_newspaper(self, paper: Newspaper):
        old_paper = self.get_newspaper(paper.paper_id)
        if old_paper is not None:
            old_paper.name = paper.name
            old_paper.frequency = paper.frequency
            old_paper.price = paper.price
        else:
            raise ValueError(f"A newspaper with ID {paper.paper_id} does not exist")
        def get_issues(self):
            return self.issues
        def add_issue(self, issue: Issue):
            self.issues.append(issue)