
class Issue(object):

    def __init__(self, publicationDate, released: bool = False):
        self.publication_date = publicationDate
        self.released: bool = released
        self.editor = None


    def set_editor(self, editor):
        self.editor = editor

    def update_issue(self):
        pass

