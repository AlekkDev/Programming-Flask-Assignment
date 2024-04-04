class Subscriber(object):
    def __init__(self, subscriber_id,name,address):
        self.subscriber_id = subscriber_id
        self.name = name
        self.address = address
        self.list_of_newspapers = []
    def get_info(self):
        return self.subscriber_id, self.name, self.address, self.list_of_newspapers
    def add_newspaper(self, newspaper):
        self.list_of_newspapers.append(newspaper)
    def update_info(self, name, address):
        self.name = name
        self.address = address
    def delete(self, subscriber):
        self.subscribers.remove(subscriber)