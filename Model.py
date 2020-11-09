from marshmallow import fields, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, event):
        for key, value in event.items():
            setattr(self, key, value)


class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    ticket_type = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, ticket_type, price):
        self.ticket_type = ticket_type
        self.price = price


class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'))
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, date):
        self.date = date


class EventSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    date = fields.DateTime()


class TicketSchema(ma.Schema):
    id = fields.Integer()
    event_id = fields.Integer(required=True)
    ticket_type = fields.String(required=True)


class ReservationSchema(ma.Schema):
    id = fields.Integer()
    ticket_id = fields.Integer(required=True)
    date = fields.String(required=True)
