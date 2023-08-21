from app import db
from app.utility import string_validation as s_v
from sqlalchemy import or_

class CONTACT(db.Model):
    contact_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), unique = True)
    email = db.Column(db.String(), unique = True)
    phone_number = db.Column(db.String(), unique=True)

    def __repr__(self):
        return f'<Contact {self.name}>'

    def change(self, name = None, email = None, phone_number = None):
        if not s_v.phone_format(phone_number):
            return 1
        if not s_v.email_format(email):
            return 2
        if CONTACT.query.filter(or_(CONTACT.name == name, CONTACT.phone_number == phone_number, CONTACT.email == email), CONTACT.contact_id != self.contact_id).first() is not None:
            return 3

        self.name = name
        self.email = email
        self.phone_number = phone_number

        return 0

    def validate(self):

        if not s_v.phone_format(self.phone_number):
            return 1
        if not s_v.email_format(self.email):
            return 2
        if CONTACT.query.filter(or_(CONTACT.name == self.name, CONTACT.phone_number == self.phone_number, CONTACT.email == self.email)).first() is not None:
            return 3

        return 0

    def dict(self):
        return {
            'contact_id' : self.contact_id,
            'name' : self.name,
            'email' : self.email,
            'phone_number' : self.phone_number,
        }