from typing import List, Union, Optional

from .newspaper import Newspaper
from .issue import Issue
from .editor import Editor
from .subscriber import Subscriber
import random

class Agency(object):
    singleton_instance = None
    def __init__(self):
        self.newspapers: List[Newspaper] = []
        self.editors: List[Editor] = []
        self.subscribers: List[Subscriber] = []

    def generate_product_id():
        # Define the range for the product ID (adjust min and max values as needed)
        # Could be done using UUID, but for simplicity, Im using a random integer from the random module
        min_id = 1000
        max_id = 9999

        # Generate a random integer within the specified range
        product_id = random.randint(min_id, max_id)

        return product_id
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
        print("update newspaper called")
        old_paper = self.get_newspaper(paper.paper_id)
        if old_paper is not None:
            old_paper.name = paper.name
            old_paper.frequency = paper.frequency
            old_paper.price = paper.price
            print(old_paper.paper_id, old_paper.name, old_paper.frequency, old_paper.price)
            return old_paper
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
        raise ValueError(f"An editor with ID {editor_id} does not exist")

    def delete_editor(self, editor):
        # FIX to satisfy "When an editor is removed (e.g., quits the job), transfer all issues in his/her supervision to another editor of the same newspaper."
        for newspaper in self.newspapers:
            for issue in newspaper.issues:
                if issue.editor_id == editor.editor_id:
                    other_editor =  newspaper.get_other_editor(editor.editor_id)
                    issue.editor_id = other_editor
        # editor.
        self.editors.remove(editor)
    def update_editor(self, editor):
        editing_editor = self.get_editor_by_id(editor.editor_id)
        if editing_editor is not None:
            editing_editor.update_info(editor.name, editor.address)
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
    def update_subscriber_info(self, subscriber):
        editing_subscriber = self.get_subscriber_by_id(subscriber.subscriber_id)
        if editing_subscriber is not None:
            editing_subscriber.name = subscriber.name
            editing_subscriber.address = subscriber.address
        else:
            raise ValueError(f"A subscriber with ID {subscriber.subscriber_id} does not exist")
    def delete_subscriber(self, subscriber):
        subscriber.clear_newspaper_history()
        self.subscribers.remove(subscriber)


    def deliver_issue_to_subscribers(self, newspaper_id, issue_id):
        for subscriber in self.subscribers:
            subscriber.receive_issue(newspaper_id, issue_id)
    def release_issue(self, newspaper_id, issue_id):
        newspaper = self.get_newspaper(newspaper_id)
        issue = newspaper.get_issue_by_id(issue_id)
        issue.release_issue()

    def get_subscriber_statistics(self,subscriber_id):
        # price_stats_dictionary = {}
        total_monthly_price = 0
        total_annual_price = 0
        #GET SUBSCRIBER BY ID
        subscriber = self.get_subscriber_by_id(subscriber_id)
        subscriber_newspapers = subscriber.list_of_newspapers
        #FOR LOOP -> GETS NEWSPAPER PRICE AND FREQUENCY FOR EACH NEWSPAPER
        for newpaper in subscriber_newspapers:
            newspaper = self.get_newspaper(newpaper)
            monthly_price, annual_price = newspaper.get_price_info()
            total_monthly_price += monthly_price
            total_annual_price += annual_price
        num_of_newspapers = len(subscriber_newspapers)

        issues_received = subscriber.issues_received_by_newspaper

        return ({"Monthly cost":total_monthly_price, "Annual cost":total_annual_price, "Number of newspaper subscriptions":num_of_newspapers}, issues_received)
    def check_for_undelivered_issues(self,subscriber_id):
        subscriber = self.get_subscriber_by_id(subscriber_id)
        for newspaper_id in subscriber.list_of_newspapers:
            newspaper = self.get_newspaper(newspaper_id)
            # print(len(newspaper.issues), len(subscriber.issues_ids_received))
            if len(newspaper.issues) != len(subscriber.issues_ids_received):
                return True
            return False
