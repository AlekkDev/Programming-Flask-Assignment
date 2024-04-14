from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields

from ..model.agency import Agency
from ..model.subscriber import Subscriber
subscriber_ns = Namespace("subscriber", description="Subscriber related operations")

subscriber_model = subscriber_ns.model('SubscriberModel', {
    'subscriber_id': fields.Integer(required=False,
            help='The unique identifier of a subscriber'),
    'name': fields.String(required=True,
            help='The name of the subscriber, e.g. Bart Simpson'),
    'address': fields.String(required=True,
            help='The address of the subscriber, e.g. First Street'),
})

@subscriber_ns.route('/')
class SubscriberAPI(Resource):

    @subscriber_ns.doc(subscriber_model, description="Add a new subscriber")
    @subscriber_ns.expect(subscriber_model, validate=True)
    @subscriber_ns.marshal_with(subscriber_model, envelope='subscriber')
    def post(self):
        # TODO_DONE: use uuid to generate a unique ID
        subscriber_id = Agency.generate_product_id()

        # create a new subscriber object with payload data and add it
        new_subscriber = Subscriber(subscriber_id=subscriber_id,
                            name=subscriber_ns.payload['name'],
                            address=subscriber_ns.payload['address'])
        Agency.get_instance().add_subscriber(new_subscriber)

        return new_subscriber

    @subscriber_ns.doc(description="Get all subscribers")
    @subscriber_ns.marshal_list_with(subscriber_model, envelope='subscribers')
    def get(self):
        return Agency.get_instance().get_all_subscribers()
@subscriber_ns.route('/<int:subscriber_id>')
class SubscriberID(Resource):

    @subscriber_ns.doc(description="Get a specific subscriber")
    @subscriber_ns.marshal_with(subscriber_model, envelope='subscriber')
    def get(self, subscriber_id):
        search_result = Agency.get_instance().get_subscriber_by_id(subscriber_id)
        if search_result == ValueError:
            return "Subscriber not found", 404
        return search_result

    @subscriber_ns.doc(parser=subscriber_model, description="Update a subscriber")
    @subscriber_ns.expect(subscriber_model, validate=True)
    @subscriber_ns.marshal_with(subscriber_model, envelope='subscriber')
    def post(self, subscriber_id):
        updated_subscriber = Subscriber(subscriber_id=subscriber_id,
                            name=subscriber_ns.payload['name'],
                            address=subscriber_ns.payload['address'])
        Agency.get_instance().update_subscriber_info(updated_subscriber)
        return updated_subscriber
    @subscriber_ns.doc(description="Delete a subscriber")
    def delete(self, subscriber_id):
        targeted_subscriber = Agency.get_instance().get_subscriber_by_id(subscriber_id)
        if not targeted_subscriber:
            return jsonify(f"Subscriber with ID {subscriber_id} was not found")
        Agency.get_instance().delete_subscriber(targeted_subscriber)
        return jsonify(f"Subscriber with ID {subscriber_id} was removed")
@subscriber_ns.route('/<int:subscriber_id>/subscribe')
class SubscriberSubscribe(Resource):
    @subscriber_ns.doc(description="Subscribe a subscriber to a newspaper")
    def post(self, subscriber_id):
        newspaper_id = subscriber_ns.payload["newspaper_id"]
        subscriber = Agency.get_instance().get_subscriber_by_id(subscriber_id)

        if subscriber is None:
            return "Subscriber not found", 404
        subscriber.subscribe_to(int(newspaper_id))
        return subscriber.get_info(),200

# @subscriber_ns.route('/<int:subscriber_id>/subscribe')
# class SubscriberSubscribe(Resource):
#     @subscriber_ns.doc(description="Subscribe a subscriber to a newspaper")
#     @subscriber_ns.expect(subscriber_model, validate=True)
#     def post(self, subscriber_id):
#         return subscriber_id, 200
#         newspaper_id = subscriber_ns.payload["newspaper_id"]
#         subscriber = Agency.get_instance().get_subscriber_by_id(subscriber_id)
#
#         if subscriber is None:
#             return "Subscriber not found", 404
#         subscriber.subscribe_to(int(newspaper_id))
#         return subscriber.get_info(),200
@subscriber_ns.route('/<int:subscriber_id>/stats')
class SubscriberStats(Resource):
    @subscriber_ns.doc(description="Get statistics for a subscriber")
    def get(self, subscriber_id):
        subs_id = subscriber_id
        subscriber = Agency.get_instance().get_subscriber_by_id(subscriber_id)
        if subscriber is None:
            return "Subscriber not found", 404
        stats = Agency.get_instance().get_subscriber_statistics(subscriber_id)

        return stats, 200
@subscriber_ns.route('/<int:subscriber_id>/missingissues')
class SubscriberMissingIssues(Resource):
    @subscriber_ns.doc(description="Get missing issues for a subscriber")
    def get(self, subscriber_id):
        subscriber = Agency.get_instance().get_subscriber_by_id(subscriber_id)
        if subscriber is None:
            return "Subscriber not found", 404
        if Agency.get_instance().check_for_undelivered_issues(subscriber_id):
            return "There are missing issues", 200
        else:
            return "There are no missing issues", 200

