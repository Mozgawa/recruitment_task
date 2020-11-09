from flask import request
from flask import Flask
from flask_restplus import Api, Resource
from Model import db, Event, EventSchema, Ticket, TicketSchema, Reservation, ReservationSchema
from flask_restplus import fields


app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)

api = Api(app=app)

ns_event = api.namespace('events', description='Event operations')
ns_ticket = api.namespace('tickets', description='Ticket operations')
ns_reservation = api.namespace('reservations', description='Reservation operations')

events_schema = EventSchema(many=True)
event_schema = EventSchema()
tickets_schema = TicketSchema(many=True)
ticket_schema = TicketSchema()
reservations_schema = ReservationSchema(many=True)
reservation_schema = ReservationSchema()

event_ = api.model('Event', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of an event'),
    'name': fields.String(required=True, description='Event name'),
    'date': fields.DateTime(required=True, description='Date and time of an  event')
})

ticket_ = api.model('Ticket', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a ticket'),
    'event_id': fields.Integer(required=True, description='The unique identifier of an event'),
    'reservation_id': fields.Integer(required=True, description='The unique identifier of an reservation'),
    'ticket_type': fields.String(required=True, description='Type of the ticket')
})

reservation_ = api.model('Reservation', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a reservation'),
    'ticket_id': fields.Integer(required=True, description='The unique identifier of a ticket'),
    'date': fields.Integer(required=True, description='The date and time of an reservation')
})

# ticket_type_ = api.model('Ticket Type', {
#     'id': fields.Integer(readOnly=True, description='The unique identifier of a ticket type'),
#     'price': fields.Float(required=True, description='Price of ticket'),
#     'ticket_type': fields.String(required=True, default='Regular', example='Regular, Premium, VIP',
#                                  description='Type of the ticket')
# })

# customer_ = api.model('Customer', {
#     'id': fields.Integer(readOnly=True, description='The unique identifier of a customer'),
#     'name': fields.String(required=True, description='Name of a customer'),
#     'phone': fields.Integer(required=True, description='Phone number of a customer')
# })


@ns_event.route("/")
class EventList(Resource):
    def get(self):
        """
        Returns a list of events
        """
        events = Event.query.all()
        events = events_schema.dump(events).data
        return {'data': events}, 200

    @api.expect(event_)
    @api.response(201, 'Event successfully created.')
    def post(self):
        """
        Adds a new event to the list
        """
        event_json = request.json
        event = Event(event_json)
        db.session.add(event)
        db.session.commit()
        return {"data": event}, 201


@ns_event.route("/<string:name>")
class EventSingle(Resource):
    @api.response(201, 'Event successfully viewed.')
    def get(self, name):
        """
        Displays an event's details
        """
        events = Event.query.filter_by(name=name).all()
        events = events_schema.dump(events).data
        return {'data': events}, 200

    @api.expect(event_)
    @api.response(201, 'Event successfully changed.')
    def put(self, name):
        """
        Changes an event's details
        """
        event = Event.query.filter_by(name=name).first()
        event_json = request.json
        event.name = event_json["name"]
        db.session.commit()
        return None, 200

    @api.response(201, 'Event successfully deleted.')
    def delete(self, name):
        """
        Deletes an event from the list
        """
        Event.query.filter_by(name=name).delete()
        db.session.commit()
        return None, 201


@ns_ticket.route("/")
class TicketList(Resource):
    @api.expect(ticket_)
    def get(self):
        """
        Returns a list of tickets
        """
        tickets = Ticket.query.all()
        tickets = ticket_schema.dump(tickets).data
        return {'data': tickets}, 200


@ns_ticket.route("/<string:event_id>")
class TicketSingle(Resource):
    def get(self, event_id):
        """
        Displays an ticket's details
        """
        tickets = Ticket.query.filter_by(id=event_id).all()
        tickets = ticket_schema.dump(tickets).data
        return {'data': tickets}, 200


@ns_reservation.route("/")
class ReservationList(Resource):
    def get(self):
        """
        Returns a list of reservations
        """
        reservations = Reservation.query.all()
        reservations = reservation_schema.dump(reservations).data
        return {'data': reservations}, 200


if __name__ == "__main__":
    app.run(debug=True)
