from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields

from ..model.agency import Agency
from ..model.newspaper import Newspaper
from ..model.issue import Issue
from ..model.editor import Editor

import random
editor_ns = Namespace("editor", description="Editor related operations")

editor_model = editor_ns.model('EditorModel', {
    'editor_id': fields.Integer(required=True,
            help='The unique identifier of an editor'),
    'name': fields.String(required=True,
            help='The name of the editor, e.g. John Doe'),
    'address': fields.String(required=True,
            help='The address of the editor, e.g. 123 Main St'),
   })


@editor_ns.route('/')
class EditorAPI(Resource):

    @editor_ns.doc(editor_model, description="Add a new editor")
    @editor_ns.expect(editor_model, validate=True)
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def post(self):
        # TODO_DONE: use uuid to generate a unique ID
        editor_id = Agency.generate_product_id()

        # create a new editor object with payload data and add it
        new_editor = Editor(editor_id=editor_id,
                            name=editor_ns.payload['name'],
                            address=editor_ns.payload['address'])
        # return new_editor.get_info()
        Agency.get_instance().add_editor(new_editor)

        return new_editor, 201

    @editor_ns.doc(editor_model, description="Get all editors")
    @editor_ns.marshal_list_with(editor_model, envelope='editors')
    def get(self):
        return Agency.get_instance().get_all_editors()
@editor_ns.route('/<int:editor_id>')
class EditorID(Resource):

    @editor_ns.doc(description="Get a specific editor")
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def get(self, editor_id):
        search_result = Agency.get_instance().get_editor_by_id(editor_id)
        if search_result == ValueError:
            return "Editor not found", 404
        return search_result

    @editor_ns.doc(parser=editor_model, description="Update an editor")
    @editor_ns.expect(editor_model, validate=True)
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def post(self, editor_id):
        updated_editor = Editor(editor_id=editor_id,
                                name=editor_ns.payload['name'],
                                address=editor_ns.payload['address'])
        return Agency.get_instance().update_editor(updated_editor)
    def delete(self, editor_id):
        targeted_editor = Agency.get_instance().get_editor_by_id(editor_id)
        if targeted_editor == ValueError:
            return f"Editor with ID {editor_id} not found", 404
        Agency.get_instance().delete_editor(targeted_editor)
        return f"Editor with ID {editor_id} was deleted", 200
@editor_ns.route('/<int:editor_id>/issues')
class EditorIssues(Resource):
    def get(self, editor_id):
        editor = Agency.get_instance().get_editor_by_id(editor_id)
        return editor.get_newspapers()
