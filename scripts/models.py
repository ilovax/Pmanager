from mongoengine import StringField,EmailField,DynamicDocument 

# account collection
class Account(DynamicDocument):
    name = StringField(max_length=50, required=True)
    password = StringField(max_length=200, required=True)
    username = StringField(max_length=50)
    email = EmailField()
