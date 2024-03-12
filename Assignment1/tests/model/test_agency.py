import pytest

from ...src.model.newspaper import Newspaper
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


