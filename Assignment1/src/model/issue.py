import datetime
class Issue(object):

    def __init__(self,issue_id, title, editor_id = None,publicationDate = datetime.datetime.now().date(), delivered: bool = False):
        self.issue_id = issue_id
        self.title = title
        self.editor_id = editor_id
        self.publication_date = publicationDate
        self.delivered: bool = delivered
        self.released = False

    def add_editor(self, editor):
        self.editor_id = editor
    def release_issue(self):
        self.released = True
    def get_info_of_issue(self):
        return self.issue_id, self.title, self.publication_date, self.editor_id, self.delivered
    def deliver_issue(self):
        self.delivered = True
    def deliver_issue_to_subscribers(self, newspaper_id, issue_id):
        for subscriber in self.subscribers:
            if newspaper_id in subscriber.list_of_newspapers:
                subscriber.messages.append(issue_id)
