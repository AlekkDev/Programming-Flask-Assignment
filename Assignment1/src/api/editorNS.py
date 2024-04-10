from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields

from ..model.agency import Agency
from ..model.newspaper import Newspaper
from ..model.issue import Issue
from ..model.editor import Editor

import random
editor_ns = Namespace("editor", description="Editor related operations")

editor_model = editor_ns.model('EditorModel', {
    'editor_id': fields.Integer(required=False,
            help='The unique identifier of an editor'),
    'name': fields.String(required=True,
            help='The name of the editor, e.g. John Doe'),
    'address': fields.String(required=True,
            help='The address of the editor, e.g. 123 Main St'),
    'list_of_newspapers': fields.List(fields.Integer, required=False,
            help='A list of newspaper IDs that the editor is responsible for')
   })


@editor_ns.route('/')
class Editor_API(Resource):
    @editor_ns.doc(editor_model, description="Add a new editor")
    @editor_ns.expect(editor_model, validate=True)
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def post(self):
        pass
        # parser = reqparse.RequestParser()
        # parser.add_argument('name', type=str, required=True, help='Name of the editor')
        # parser.add_argument('address', type=str, required=True, help='Address of the editor')
        # args = parser.parse_args()
        # editor = Editor(args['name'], args['address'])
        # agency.add_editor(editor)
        # return editor, 201

    @editor_ns.doc(editor_model, description="Get all editors")
    @editor_ns.marshal_list_with(editor_model, envelope='editor')
    def get(self):
        pass
        # return agency.get_all_editors(), 200

