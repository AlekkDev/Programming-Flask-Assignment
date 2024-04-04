import pytest

from ...src.model.newspaper import Newspaper
from ...src.model.issue import Issue
from ...src.model.editor import Editor
from ...src.model.subscriber import Subscriber
from ..fixtures import app, client, agency


def test_add_newspaper(agency):
    before = len(agency.newspapers)
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    assert len(agency.all_newspapers()) == before + 1


def test_add_newspaper_same_id_should_raise_error(agency):
    before = len(agency.newspapers)
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)

    # first adding of newspaper should be okay
    # agency.add_newspaper(new_paper)

    new_paper2 = Newspaper(paper_id=999,
                          name="Superman Comic",
                          frequency=7,
                          price=13.14)

    with pytest.raises(ValueError, match='A newspaper with ID 999 already exists'):  # <-- this allows us to test for exceptions
        # this one should rais ean exception!
        agency.add_newspaper(new_paper2)
def test_remove_newspaper(agency):
    before = len(agency.newspapers)
    new_paper = Newspaper(paper_id=123,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    assert len(agency.all_newspapers()) == before + 1
    agency.remove_newspaper(new_paper)
    assert len(agency.all_newspapers()) == before
def test_update_newspaper(agency):
    old_paper = Newspaper(paper_id=123,
                            name="Simpsons Comic",
                            frequency=7,
                            price=3.14)
    agency.add_newspaper(old_paper)
    new_paper = Newspaper(paper_id=123,
                          name="Simpsons Drama",
                          frequency=13,
                          price=5)
    agency.update_newspaper(new_paper)
    assert new_paper.name == "Simpsons Drama" and new_paper.frequency == 13 and new_paper.price == 5

def test_create_issue_and_get_issue(agency):
    new_paper = Newspaper(paper_id=444,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    new_issue = Issue(issue_id=123,publicationDate="2021-09-01", title="Stiegl is overrated" )
    agency.add_newspaper(new_paper)
    new_paper.add_issue(new_issue)
    assert len(new_paper.get_issues()) == 1
def test_get_info_of_issue(agency):
    new_paper = Newspaper(paper_id=445,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    new_issue = Issue(issue_id=123,publicationDate="2023-09-01", title="Stiegl is definitely not overrated" )
    agency.add_newspaper(new_paper)
    new_paper.add_issue(new_issue)
    assert new_paper.get_issue_by_id(123).title == "Stiegl is definitely not overrated" and new_paper.get_issue_by_id(123).publication_date == "2023-09-01"

def test_create_and_delete_editor(agency):
    new_paper = Newspaper(paper_id=464,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    new_editor = Editor(editor_id=1, name="Homer Simpson",address="First Street",list_of_newspapers=[])
    agency.add_newspaper(new_paper)
    agency.add_editor(new_editor)
    new_issue = Issue(issue_id=123,publicationDate="2023-09-01", title="Stiegl is definitely not overrated" )
    new_issue.add_editor(new_editor)
    assert agency.get_editor_by_id(new_editor.editor_id) == new_editor
    agency.delete_editor(new_editor)
    assert agency.get_editor_by_id(new_editor.editor_id) == None
def test_get_editor_info(agency):
    new_paper = Newspaper(paper_id=465,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    new_editor = Editor(editor_id=1, name="Homer Simpson",address="First Street",list_of_newspapers=[])
    agency.add_newspaper(new_paper)
    agency.add_editor(new_editor)
    assert new_editor.get_info() == (1,"Homer Simpson","First Street",[])
def test_add_editor_to_issue(agency):
    new_paper = Newspaper(paper_id=435,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    new_issue = Issue(issue_id=123,publicationDate="2023-09-01", title="Stiegl is definitely not overrated" )
    agency.add_newspaper(new_paper)
    new_editor = Editor(editor_id=2, name="Homer Simpson", address="First Street", list_of_newspapers=[])
    new_paper.add_issue(new_issue)
    new_issue.add_editor(new_editor.editor_id)
    assert new_issue.editor_id == new_editor.editor_id
def test_update_editor(agency):
    new_paper = Newspaper(paper_id=467,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    new_editor = Editor(editor_id=2, name="Homer Simpson", address="First Street")
    agency.add_newspaper(new_paper)
    agency.add_editor(new_editor)
    agency.get_editor_by_id(2).update_info(name = "Bart Simpson", address = "Second Street")
    assert agency.get_editor_by_id(2).get_info() == (2,"Bart Simpson","Second Street",[])
def test_get_editor_newspapers(agency):
    new_paper = Newspaper(paper_id=468,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    new_editor = Editor(editor_id=2, name="Homer Simpson", address="First Street")
    agency.add_newspaper(new_paper)
    agency.add_editor(new_editor)
    new_editor.add_newspaper(new_paper)
    assert new_editor.get_newspapers() == [new_paper]

def test_get_all_subscribers(agency):
    new_paper = Newspaper(paper_id=469,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    new_subscriber = Subscriber(subscriber_id=1, name="Bart Simpson", address="First Street")
    agency.add_newspaper(new_paper)
    agency.add_subscriber(new_subscriber)
    assert len(agency.get_all_subscribers()) == 1

