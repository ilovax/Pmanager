from mongoengine import StringField,EmailField,Document 

# account collection
class Account(Document):
    name = StringField(max_length=50, required=True)
    password = StringField(max_length=200, required=True)
    username = StringField(max_length=50)
    email = EmailField()
    iv = StringField(max_length=200, required=True)
