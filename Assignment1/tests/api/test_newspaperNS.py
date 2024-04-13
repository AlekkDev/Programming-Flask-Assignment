# import the fixtures (this is necessary!)
from ..fixtures import app, client, agency
from ...src.model.issue import Issue
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
    response = client.post("/newspaper/",  # <-- note the slash at the end!
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
    response = client.get(f"/newspaper/{paper.paper_id}")  # <-- note the slash at the end!

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
    response = client.post(f"/newspaper/{paper.paper_id}",  # <-- note the slash at the end!
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
    response = client.delete(f"/newspaper/{paper.paper_id}")  # <-- note the slash at the end!
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
    response = client.get(f"/newspaper/{paper.paper_id}/issue")  # <-- note the slash at the end!

    # verify
    assert response.status_code == 200
    parsed = response.get_json()
    issues = parsed
    assert len(issues) == len(paper.issues)
def test_add_issue_to_newspaper(client, agency):
    # prepare
    paper = agency.newspapers[0]
    issue_count_before = len(paper.get_issues())

    response = client.post(f"/newspaper/{paper.paper_id}/issue",  # <-- note the slash at the end!
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
    response = client.get(f"/newspaper/{paper.paper_id}/issue/{issue.issue_id}")  # <-- note the slash at the end!

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
    response = client.post(f"/newspaper/{paper.paper_id}/issue/{issue.issue_id}/release")  # <-- note the slash at the end!

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
