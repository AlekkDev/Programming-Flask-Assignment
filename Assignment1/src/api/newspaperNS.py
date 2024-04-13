from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields

from ..model.agency import Agency
from ..model.newspaper import Newspaper
from ..model.issue import Issue
from ..model.editor import Editor

import random

newspaper_ns = Namespace("newspaper", description="Newspaper related operations")

paper_model = newspaper_ns.model('NewspaperModel', {
    'paper_id': fields.Integer(required=False,
            help='The unique identifier of a newspaper'),
    'name': fields.String(required=True,
            help='The name of the newspaper, e.g. The New York Times'),
    'frequency': fields.Integer(required=True,
            help='The publication frequency of the newspaper in days (ex. 1 for daily papers and 7 for weekly magazines'),
    'price': fields.Float(required=True,
            help='The monthly price of the newspaper (e.g. 12.3)')
   })
issue_model = newspaper_ns.model('IssueModel', {
    'issue_id': fields.Integer(required=False,
            help='The unique identifier of an issue'),
    'publication_date': fields.String(required=True,
            help='The date of the issue, e.g. 2021-01-01'),
    'title': fields.String(required=True,
            help='The title of the issue, e.g. "The world is ending"'),
    'editor_id': fields.Integer(required=False,
                               help='The unique identifier of the editor of the issue'),
    'delivered': fields.Boolean(required=False,
                                help='A boolean indicating if the issue was delivered or not')
   })

subscriber_model = newspaper_ns.model('SubscriberModel', {
    'subscriber_id': fields.Integer(required=False,
            help='The unique identifier of a subscriber'),
    'name': fields.String(required=True,
            help='The name of the subscriber, e.g. Bart Simpson'),
    'address': fields.String(required=True,
            help='The address of the subscriber, e.g. First Street'),
})

@newspaper_ns.route('/')
class NewspaperAPI(Resource):

    @newspaper_ns.doc(paper_model, description="Add a new newspaper")
    @newspaper_ns.expect(paper_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self):
        # TODO_DONE: use uuid to generate a unique ID
        paper_id = Agency.generate_product_id()

        # create a new paper object and add it
        new_paper = Newspaper(paper_id=paper_id,
                              name=newspaper_ns.payload['name'],
                              frequency=newspaper_ns.payload['frequency'],
                              price=newspaper_ns.payload['price'])
        Agency.get_instance().add_newspaper(new_paper)

        # return the new paper
        return new_paper

    @newspaper_ns.doc(description="Get all newspapers")
    @newspaper_ns.marshal_list_with(paper_model, envelope='newspapers')
    def get(self):
        return Agency.get_instance().all_newspapers()

@newspaper_ns.route('/<int:paper_id>')
class NewspaperID(Resource):

    @newspaper_ns.doc(description="Get a specific newspaper")
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def get(self, paper_id):
        search_result = Agency.get_instance().get_newspaper(paper_id)
        return search_result

    @newspaper_ns.doc(parser=paper_model, description="Update a new newspaper")
    @newspaper_ns.expect(paper_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self, paper_id):
        updated_paper = Newspaper(paper_id=paper_id,
                                  name=newspaper_ns.payload['name'],
                                  frequency=newspaper_ns.payload['frequency'],
                                  price=newspaper_ns.payload['price'])
        # print(updated_paper)
        return Agency.get_instance().update_newspaper(updated_paper)

    @newspaper_ns.doc(description="Delete a new newspaper")
    def delete(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        Agency.get_instance().remove_newspaper(targeted_paper)
        return jsonify(f"Newspaper with ID {paper_id} was removed")
@newspaper_ns.route('/<int:paper_id>/issue')
class NewspaperIssueAPI(Resource):
    @newspaper_ns.doc(description="Get all issues of a newspaper")
    def get(self, paper_id):
        paper = Agency.get_instance().get_newspaper(paper_id)
        return paper.get_issues()

    @newspaper_ns.doc(issue_model, description="Create an issue of a newspaper")
    @newspaper_ns.expect(issue_model, validate=True)
    @newspaper_ns.marshal_with(issue_model, envelope='issue')
    def post(self, paper_id):
        paper = Agency.get_instance().get_newspaper(paper_id)
        paper.add_issue(newspaper_ns.payload)
        # print(newspaper_ns.payload)
        return newspaper_ns.payload
@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>')
class NewspaperIssueID(Resource):
    @newspaper_ns.doc(description="Get a specific issue of a newspaper")
    @newspaper_ns.marshal_with(issue_model, envelope='issue')
    def get(self, paper_id, issue_id):
        paper = Agency.get_instance().get_newspaper(paper_id)
        return paper.get_issue_by_id(issue_id)
@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>/release')
class NewspaperIssueRelease(Resource):
    @newspaper_ns.doc(description="Release a specific issue of a newspaper")
    def post(self, paper_id, issue_id):
        paper = Agency.get_instance().get_newspaper(paper_id)
        issue = paper.get_issue_by_id(issue_id)
        issue.release_issue()
        return jsonify(issue.get_info_of_issue())




