# import the fixtures (this is necessary!)
from ..fixtures import app, client, agency

import pytest
from ...src.model.editor import Editor
from ...src.model.agency import Agency
from ...src.model.newspaper import Newspaper

def test_add_editor(client, agency):
    # prepare
    editor_count_before = len(agency.editors)

    # act
    response = client.post("/editor/",
                           json={
                                "editor_id": 1,
                               "name": "John Doe",
                               "address": "123 Elm Street"
                           })
    print(response.get_json())
    assert response.status_code == 201

    # verify
    assert len(agency.editors) == editor_count_before + 1
    parsed = response.get_json()
    editor_response = parsed["editor"]

    # verify that the response contains the newspaper data
    assert editor_response["name"] == "John Doe"
    assert editor_response["address"] == "123 Elm Street"
def test_get_all_editors(client, agency):
    # prepare
    response = client.get("/editor/")
    assert response.status_code == 200
    parsed = response.get_json()
    editors = parsed["editors"]
    assert len(editors) == len(agency.get_all_editors())

def test_get_editor_by_id(client, agency):
    # prepare
    editor = agency.editors[0]

    # act
    response = client.get(f"/editor/{editor.editor_id}")

    # verify
    assert response.status_code == 200
    parsed = response.get_json()
    editor_response = parsed["editor"]

    # verify that the response contains the newspaper data
    assert editor_response["name"] == editor.name
    assert editor_response["address"] == editor.address
def test_get_info_of_editor(client, agency):
    # prepare
    editor = agency.editors[0]

    # act
    response = client.get(f"/editor/{editor.editor_id}")

    # verify
    assert response.status_code == 200
    parsed = response.get_json()
    editor_response = parsed["editor"]

    # verify that the response contains the newspaper data
    assert editor_response["name"] == editor.name
    assert editor_response["address"] == editor.address

def test_update_editor(client, agency):
    editor = agency.editors[0]
    response = client.post(f"/editor/{editor.editor_id}",
                           json={
                               "name": "John Doe",
                               "address": "123 Elm Street"
                           })
def atest_editor_not_found(client, agency):
    response = client.get("/editor/99999")
    assert response.status_code == 404
    parsed = response.get_json()
    assert parsed == f"Editor with ID 99999 not found"


    # verify that the response contains the newspaper data
    # assert parsed == f"Editor with ID {editor.editor_id} was deleted"


    # print(parsed)
    # verify that the response contains the newspaper data

def test_get_newspapers_of_editor(client, agency):
    # prepare
    editor = agency.editors[0]

    # act
    response = client.get(f"/editor/{editor.editor_id}/issues")

    # verify
    assert response.status_code == 200
    parsed = response.get_json()
    assert parsed == editor.get_newspapers()


def test_delete_editor(client, agency):
    # prepare
    editor_count_before = len(agency.editors)
    editor = agency.editors[0]

    # act
    response = client.delete(f"/editor/{editor.editor_id}")
    assert response.status_code == 200

    # verify
    assert len(agency.editors) == editor_count_before - 1

    # print(parsed)
