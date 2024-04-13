class Subscriber(object):
    def __init__(self, subscriber_id,name,address):
        self.subscriber_id = subscriber_id
        self.name = name
        self.address = address
        self.list_of_newspapers = []
        self.messages = []
        self.issues_ids_received = []
        self.issues_received_by_newspaper = {}
    def get_info(self):
        return self.subscriber_id, self.name, self.address, self.list_of_newspapers
    def subscribe_to(self, newspaper_id):
        try:
            newspaper_id = int(newspaper_id)
            self.list_of_newspapers.append(newspaper_id)
        except:
            raise ValueError("Newspaper ID must be an integer")
    def update_info(self, name, address):
        self.name = name
        self.address = address
    def receive_issue(self, newspaper_id, issue_id):

        self.messages.append(f"New issue of {newspaper_id} is available")
        self.issues_ids_received.append(issue_id)
        # print(self.issues_received_by_newspaper)
        if newspaper_id not in self.issues_received_by_newspaper.keys():
            self.issues_received_by_newspaper[newspaper_id] = 1
            return self.issues_received_by_newspaper
        else:
            value = self.issues_received_by_newspaper[newspaper_id]
            self.issues_received_by_newspaper[newspaper_id] = value + 1
            return self.issues_received_by_newspaper
    def clear_newspaper_history(self):
        self.issues_received_by_newspaper = {}
        self.messages = []
        self.issues_ids_received = []


