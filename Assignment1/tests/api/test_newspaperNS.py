# import the fixtures (this is necessary!)
from ..fixtures import app, client, agency
from ...src.model.agency import Agency
from ...src.model.subscriber import Subscriber

# FILE WITH ALL TEST FUNCTIONS
# COULD HAVE BEEN SEPARATED INTO MORE FILES BUT I BELIEVE THERE IS NO NEED
# ALL TESTS ARE PRETTY SELF-EXPLANATORY AND ORDERED AS IN THE README FILE

def test_get_newspaper_should_list_all_papers(client, agency):
    # send request
    response = client.get("/newspaper/")   # <-- note the slash at the end!

    # test status code
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    assert len(parsed["newspapers"]) == len(agency.newspapers)


def test_add_newspaper(client, agency):
    # prepare
    paper_count_before = len(agency.newspapers)

    # act
    response = client.post("/newspaper/",
                           json={
                               "name": "Simpsons Comic",
                               "frequency": 7,
                               "price": 3.14
                           })
    assert response.status_code == 200
    # verify

    assert len(agency.newspapers) == paper_count_before + 1
    # parse response and check that the correct data is here
    parsed = response.get_json()
    paper_response = parsed["newspaper"]

    # verify that the response contains the newspaper data
    assert paper_response["name"] == "Simpsons Comic"
    assert paper_response["frequency"] == 7
    assert paper_response["price"] == 3.14
def test_get_newspaper_info(client, agency):
    # prepare
    paper = agency.newspapers[0]

    # act
    response = client.get(f"/newspaper/{paper.paper_id}")

    # verify
    assert response.status_code == 200
    parsed = response.get_json()
    paper_response = parsed["newspaper"]

    # verify that the response contains the newspaper data
    assert paper_response["name"] == paper.name
    assert paper_response["frequency"] == paper.frequency
    assert paper_response["price"] == paper.price
def test_update_newspaper(client, agency):
    # prepare
    paper = agency.newspapers[0]

    # act
    response = client.post(f"/newspaper/{paper.paper_id}",
                           json={
                               "name": "Simpsons Comic",
                               "frequency": 7,
                               "price": 3.15
                           })
    assert response.status_code == 200

    # verify
    parsed = response.get_json()
    # print(parsed)
    paper_response = parsed["newspaper"]

    # verify that the response contains the newspaper data
    assert paper_response["name"] == "Simpsons Comic"
    assert paper_response["frequency"] == 7
    assert paper_response["price"] == 3.15
def test_delete_newspaper(client, agency):
    # prepare
    paper = agency.newspapers[0]
    paper_count_before = len(agency.newspapers)

    # act
    response = client.delete(f"/newspaper/{paper.paper_id}")
    assert response.status_code == 200

    # verify
    assert len(agency.newspapers) == paper_count_before - 1
    parsed = response.get_json()
    assert parsed == f"Newspaper with ID {paper.paper_id} was removed"
def test_get_issues_of_newspaper(client, agency):
    # prepare
    paper = agency.newspapers[0]
    issue = paper.issues

    # act
    response = client.get(f"/newspaper/{paper.paper_id}/issue")

    # verify
    assert response.status_code == 200
    parsed = response.get_json()
    issues = parsed
    assert len(issues) == len(paper.issues)
def test_add_issue_to_newspaper(client, agency):
    # prepare
    paper = agency.newspapers[0]
    issue_count_before = len(paper.get_issues())

    response = client.post(f"/newspaper/{paper.paper_id}/issue",
                           json={
                               "issue_id": 1,
                               "title": "Issue 1",
                               "editor_id": 1,
                               "publication_date": "2021-10-01",
                               "delivered": False
                           })

    # verify
    parsed = response.get_json()
    issue_response = parsed["issue"]


    # verify that the response contains the newspaper data
    assert issue_response["issue_id"] == 1
    assert issue_response["title"] == "Issue 1"
    assert issue_response["editor_id"] == 1
    assert issue_response["publication_date"] == "2021-10-01"
    assert issue_response["delivered"] == False
    assert len(paper.get_issues()) == issue_count_before + 1
    # print(paper.get_issues())


def test_get_issue_of_newspaper(client, agency):
    # prepare
    paper = agency.newspapers[0]
    issue = paper.issues[0]

    # act
    response = client.get(f"/newspaper/{paper.paper_id}/issue/{issue.issue_id}")

    # verify
    assert response.status_code == 200
    parsed = response.get_json()
    issue_response = parsed["issue"]

    # verify that the response contains the newspaper data
    assert issue_response["issue_id"] == issue.issue_id
    assert issue_response["title"] == issue.title
    assert issue_response["editor_id"] == issue.editor_id
    assert issue_response["publication_date"] == str(issue.publication_date)
    assert issue_response["delivered"] == issue.delivered
def test_release_issue(client, agency):
    # prepare
    paper = agency.newspapers[0]
    issue = paper.issues[0]

    # act
    response = client.post(f"/newspaper/{paper.paper_id}/issue/{issue.issue_id}/release")

    # verify
    assert response.status_code == 200
    parsed = response.get_json()
    print(parsed)
    issue_response = parsed

    # verify that the response contains the newspaper data
    assert issue_response[0] == issue.issue_id
    assert issue_response[1] == issue.title
    assert issue_response[2] == issue.editor_id
    assert issue_response[3] == str(issue.publication_date)
    assert issue_response[4] == issue.delivered
    assert issue_response[5] == True
def test_specify_editor_for_issue(client, agency):
    paper = agency.newspapers[0]
    issue = paper.issues[0]
    # editor = agency.editors[0]
    response = client.post(f"/newspaper/{paper.paper_id}/issue/{issue.issue_id}/editor/"
                           ,json={"editor_id": 1})

    print(response)
    assert response.status_code == 200
    parsed = response.get_json()
    issue_response = parsed
    assert issue_response[0] == issue.issue_id
    assert issue_response[1] == issue.title
    assert issue_response[2] == 1
def test_deliver_issue(client, agency):
    paper = agency.newspapers[0]
    issue = paper.issues[0]
    response = client.post(f"/newspaper/{paper.paper_id}/issue/{issue.issue_id}/deliver/")
    assert response.status_code == 200
    parsed = response.get_json()
    issue_response = parsed
    assert issue_response[0] == issue.issue_id
    assert issue_response[1] == issue.title
    assert issue_response[2] == 1
    assert issue_response[3] == str(issue.publication_date)
    assert issue_response[4] == issue.delivered
    assert issue_response[5] == True

def test_get_subscribers(client, agency):
    response = client.get("/subscriber/")
    assert response.status_code == 200
    parsed = response.get_json()
    subscribers = parsed["subscribers"]
    assert len(subscribers) == len(agency.subscribers)

def test_create_subscriber(client, agency):
    subscriber_count_before = len(agency.subscribers)
    response = client.post("/subscriber/",
                           json={
                               "subscriber_id": 1,
                               "name": "John Doe",
                               "address": "123 Elm Street"
                           })
    assert response.status_code == 200
    assert len(agency.subscribers) == subscriber_count_before + 1
    parsed = response.get_json()
    subscriber_response = parsed["subscriber"]
    assert subscriber_response["name"] == "John Doe"
    assert subscriber_response["address"] == "123 Elm Street"


def test_get_subscriber_by_id(client, agency):
    subscriber = agency.subscribers[0]
    response = client.get(f"/subscriber/{subscriber.subscriber_id}")
    assert response.status_code == 200
    parsed = response.get_json()
    subscriber_response = parsed["subscriber"]
    assert subscriber_response["name"] == subscriber.name
    assert subscriber_response["address"] == subscriber.address
def test_update_subscriber(client, agency):
    subscriber = agency.subscribers[0]
    response = client.post(f"/subscriber/{subscriber.subscriber_id}",
                           json={
                               "name": "Jane Doe",
                               "address": "456 Oak Street"
                           })
    assert response.status_code == 200
    parsed = response.get_json()
    subscriber_response = parsed["subscriber"]
    assert subscriber_response["name"] == "Jane Doe"
    assert subscriber_response["address"] == "456 Oak Street"
def test_delete_subscriber(client, agency):
    subscriber = agency.subscribers[0]
    subscriber_count_before = len(agency.subscribers)
    response = client.delete(f"/subscriber/{subscriber.subscriber_id}")
    assert response.status_code == 200
    assert len(agency.subscribers) == subscriber_count_before - 1
    parsed = response.get_json()
    assert parsed == f"Subscriber with ID {subscriber.subscriber_id} was removed"

def test_subscribe_to_newspaper(client, agency):
    subscriber = Subscriber(subscriber_id=60, name="John Doe", address="123 Elm Street")
    agency.add_subscriber(subscriber)
    Newspaper = agency.newspapers[0]
    response = client.post(f"/subscriber/{subscriber.subscriber_id}/subscribe",
                           json={
                               "newspaper_id": Newspaper.paper_id
                           })
    assert response.status_code == 200
    assert subscriber.list_of_newspapers == [Newspaper.paper_id]
def test_get_subscriber_statistics(client, agency):
    subscriber = Subscriber(subscriber_id=58, name="John Doe", address="123 Elm Street")
    agency.add_subscriber(subscriber)
    Newspaper = agency.newspapers[0]
    subscriber.subscribe_to(Newspaper.paper_id)
    response = client.get(f"/subscriber/{subscriber.subscriber_id}/stats")
    assert response.status_code == 200
    parsed = response.get_json()
    assert parsed == [{'Monthly cost': 33.6, 'Annual cost': 408.8, 'Number of newspaper subscriptions': 1}, {}]
def test_check_for_undelivered_issues(client, agency):
    subscriber = Subscriber(subscriber_id=59, name="John Doe", address="123 Elm Street")
    agency.add_subscriber(subscriber)
    Newspaper = agency.newspapers[0]
    subscriber.subscribe_to(Newspaper.paper_id)
    response = client.get(f"/subscriber/{subscriber.subscriber_id}/missingissues")
    assert response.status_code == 200
    parsed = response.get_json()
    assert parsed == "There are missing issues"

