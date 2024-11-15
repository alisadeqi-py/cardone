from mongoengine import Document, StringField, BooleanField, ObjectIdField, DateTimeField, ReferenceField, CASCADE
from bson import ObjectId
from django.utils import timezone
from user.models import Dealership


# Create your models here.

class Customer(Document):
    meta = {
        'collection': 'customers',
        'indexes':['CustomerId'],
        'soft_delete': {'deleted': True}
    }
    CustomerId = ObjectIdField(default=ObjectId, db_field="_id", primary_key=True, read_only=True)
    firstName = StringField(required=True, max_length=50)
    lastName = StringField(required=True, max_length=50)
    phone = StringField(required=True, max_length=15)
    gender = StringField(required=True, choices=['Male', 'Female', 'Other'])
    dealerId = ReferenceField(Dealership, required = True, reverse_delete_rule = CASCADE)
    dateCreated = DateTimeField(default=timezone.now, read_only=True)
    dateUpdated = DateTimeField(auto_now=True, read_only=True)
    isDeleted = BooleanField(default=False)

    def __str__(self):
        # return f'{self.id}'
        return f'{self.firstName} {self.lastName}'
