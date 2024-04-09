class Subscriber(object):
    def __init__(self, subscriber_id,name,address):
        self.subscriber_id = subscriber_id
        self.name = name
        self.address = address
        self.list_of_newspapers = []
        self.messages = []
    def get_info(self):
        return self.subscriber_id, self.name, self.address, self.list_of_newspapers
    def subscribe_to(self, newspaper_id):
        try:
            newspaper_id = int(newspaper_id)
        except:
            raise ValueError("Newspaper ID must be an integer")
        self.list_of_newspapers.append(newspaper_id)
    def update_info(self, name, address):
        self.name = name
        self.address = address