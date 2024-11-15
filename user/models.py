from mongoengine import Document,CASCADE, StringField, ListField, IntField, ReferenceField, BooleanField, ObjectIdField, EmailField, DateTimeField
from bson import ObjectId
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
# from customer.models import Customer


class User(Document):
    meta = {
        'collection': 'users',
        'indexes': ['email', 'username'],
        'soft_delete': {'deleted': True}
    }
    userId = ObjectIdField(default=ObjectId, db_field="_id", primary_key=True, read_only=True)
    firstName = StringField(max_length=50)
    lastName = StringField(max_length=50)
    username = StringField(required=True, unique=True, max_length=50)
    email = EmailField(required=True, unique=True)
    phone = StringField(required=True, max_length=15)
    gender = StringField(required=True, choices=['Male', 'Female', 'Other'])
    dateCreated = DateTimeField(default=timezone.now, read_only=True)
    dateUpdated = DateTimeField(auto_now=True, read_only=True)
    isDeleted = BooleanField(default=False)
    password = StringField(required = True)

    def __str__(self):
        return f'{self.id}'
        # return f'{self.firstName} {self.lastName}'

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Dealership(Document):
    meta = {
        'collection': 'dealerships',
        # 'indexes': ['owner'],
    }
    dealerId = ObjectIdField(default=ObjectId, db_field="_id", primary_key=True, read_only=True)
    address = StringField(required=True)
    owner = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    salesVolume = IntField(required=True, min_value=0)
    domain = StringField()
    staffs = ListField(ReferenceField('User', reverse_delete_rule=CASCADE))
    phone1 = StringField(required=True)
    phone2 = StringField()
    phone3 = StringField()
    city = StringField(required=True)
    state = StringField(required=True)
    isLegal = BooleanField(default=True)
    customers = ListField(ReferenceField('User', reverse_delete_rule=CASCADE))
    dateCreated = DateTimeField(default=timezone.now, read_only=True)
    dateUpdated = DateTimeField(auto_now=True, read_only=True)
    isDeleted = BooleanField(default=False)

    def delete(self, *args, **kwargs):
        # Perform soft delete by setting isDeleted to True
        self.isDeleted = True
        self.save()

    def __str__(self):
        return f'{self.dealerId} - {self.address}'
