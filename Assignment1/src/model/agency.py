from typing import List, Union, Optional

from .newspaper import Newspaper
from .issue import Issue
from .editor import Editor
from .subscriber import Subscriber

class Agency(object):
    singleton_instance = None

    def __init__(self):
        self.newspapers: List[Newspaper] = []
        self.editors: List[Editor] = []
        self.subscribers: List[Subscriber] = []

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
    def add_editor(self, editor):
        self.editors.append(editor)
    def get_all_editors(self):
        return self.editors
    def get_editor_by_id(self,editor_id):
        for editor in self.editors:
            if editor.editor_id == editor_id:
                return editor
        return None
    def delete_editor(self, editor):
        self.editors.remove(editor)
    def update_editor(self, editor):
        editing_editor = self.get_editor_by_id(editor.editor_id)
        if editing_editor is not None:
            editing_editor.name = editor.name
            editing_editor.address = editor.address
        else:
            raise ValueError(f"An editor with ID {editor.editor_id} does not exist")
    def get_newspapers_of_editor(self, editor_id):
        editor = self.get_editor_by_id(editor_id)
        return editor.get_newspapers()

    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)
    def get_all_subscribers(self):
        subscribers = []
        for subscriber in self.subscribers:
            subscribers.append(subscriber.get_info())
        return subscribers
    def get_subscriber_by_id(self,subscriber_id):
        for subscriber in self.subscribers:
            if subscriber.subscriber_id == subscriber_id:
                return subscriber
        return None