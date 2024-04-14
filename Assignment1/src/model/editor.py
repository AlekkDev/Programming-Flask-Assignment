class Editor(object):
    def __init__(self, editor_id,name, address, list_of_newspapers = []):
        self.editor_id = editor_id
        self.name = name
        self.address = address
        self.list_of_newspapers = list_of_newspapers
    def get_info(self):
        return self.editor_id, self.name, self.address, self.list_of_newspapers
    def add_newspaper(self, newspaper):
        self.list_of_newspapers.append(newspaper)
    def remove_newspaper(self, newspaper):
        self.list_of_newspapers.remove(newspaper)
    def update_info(self, name, address):
        self.name = name
        self.address = address
    def get_newspapers(self):
        return self.list_of_newspapers
