
class Issue(object):

    def __init__(self,issue_id, title, publicationDate, editor_id = None, delivered: bool = False):
        self.issue_id = issue_id
        self.title = title
        self.publication_date = publicationDate
        self.editor_id = editor_id
        self.delivered: bool = delivered

    def add_editor(self, editor):
        self.editor_id = editor
    def release_issue(self, release_date):
        self.release_date = release_date
        self.delivered = True
    def get_info_of_issue(self):
        return self.issue_id, self.title, self.publication_date, self.editor_id, self.delivered
