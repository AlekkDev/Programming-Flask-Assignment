from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields

from ..model.agency import Agency
from ..model.newspaper import Newspaper
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

def generate_product_id():
    # Define the range for the product ID (adjust min and max values as needed)
    min_id = 1000
    max_id = 9999

    # Generate a random integer within the specified range
    product_id = random.randint(min_id, max_id)

    return product_id
@newspaper_ns.route('/')
class NewspaperAPI(Resource):

    @newspaper_ns.doc(paper_model, description="Add a new newspaper")
    @newspaper_ns.expect(paper_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self):
        # TODO_DONE: use uuid to generate a unique ID
        paper_id = generate_product_id()

        # create a new paper object and add it
        new_paper = Newspaper(paper_id=paper_id,
                              name=newspaper_ns.payload['name'],
                              frequency=newspaper_ns.payload['frequency'],
                              price=newspaper_ns.payload['price'])
        Agency.get_instance().add_newspaper(new_paper)

        # return the new paper
        return new_paper

    @newspaper_ns.marshal_list_with(paper_model, envelope='newspapers')
    def get(self):
        return Agency.get_instance().all_newspapers()

@newspaper_ns.route('/<int:paper_id>')
class NewspaperID(Resource):

    @newspaper_ns.doc(parser=paper_model, description="Get a new newspaper")
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def get(self, paper_id):
        search_result = Agency.get_instance().get_newspaper(paper_id)
        return search_result

    @newspaper_ns.doc(parser=paper_model, description="Update a new newspaper")
    @newspaper_ns.expect(paper_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self, paper_id):
        paperToUpdate = Agency.get_instance().get_newspaper(paper_id)
        if not paperToUpdate:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        else:
            paperToUpdate.name = newspaper_ns.payload['name']
            paperToUpdate.frequency = newspaper_ns.payload['frequency']
            paperToUpdate.price = newspaper_ns.payload['price']
            Agency.update_newspaper(paperToUpdate)

    @newspaper_ns.doc(description="Delete a new newspaper")
    def delete(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        Agency.get_instance().remove_newspaper(targeted_paper)
        return jsonify(f"Newspaper with ID {paper_id} was removed")
@newspaper_ns.route('/<int:paper_id>/issues')
class NewspaperAPI(Resource):

    @newspaper_ns.doc(paper_model, description="Get all issues of a newspaper")
    @newspaper_ns.marshal_list_with(issue_model, envelope='issues')
    def get(self, paper_id):
        paper = Agency.get_instance().get_newspaper(paper_id)
        return paper.get_issues()

    @newspaper_ns.doc(paper_model, description="Create an issue of a newspaper")
    @newspaper_ns.expect(issue_model, validate=True)
    @newspaper_ns.marshal_with(issue_model, envelope='issue')
    def post(self, paper_id):
        paper = Agency.get_instance().get_newspaper(paper_id)
        paper.add_issue(newspaper_ns.payload)
        return paper.get_issues()

