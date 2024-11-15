from mongoengine import Document, StringField, ListField, ObjectIdField, BooleanField, DateTimeField, ReferenceField, CASCADE
from bson import ObjectId
from django.utils import timezone
from user.models import Dealership


# Create your models here.
class Car(Document):
    meta = {
        'collection': 'cars',
        'indexes':['model'],
        'soft_delete': {'deleted': True}
    }
    CarId = ObjectIdField(default=ObjectId, db_field="_id", primary_key=True, read_only=True)
    model = StringField(required=True)
    color = StringField(required=True)
    make = StringField(required=True)
    year = StringField(max_length=50)
    milge = StringField(max_length=50)
    interiorColor = StringField(choices=['White', 'Brown', 'Black'])
    platform = StringField(max_length=50)
    isInstallment = BooleanField(default=False)
    isChecked = BooleanField(default=False)
    fuelType = StringField(choices=['Petrol', 'Gas', 'Gasoil','Electric','Dual','Hybrid'])
    vin = StringField(max_length=50)
    photos = ListField(StringField(max_length=500), default=list)  # Field to store list of photo URLs
    dealerId = ReferenceField(Dealership, required=True, reverse_delete_rule=CASCADE)
    enable = BooleanField(default=False)
    dateCreated = DateTimeField(default=timezone.now, read_only=True)
    dateUpdated = DateTimeField(auto_now=True, read_only=True)
    isDeleted = BooleanField(default=False)

    def __str__(self):
        return f'{self.id}'
