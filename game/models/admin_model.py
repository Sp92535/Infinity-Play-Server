from . import Document,StringField,bcrypt

class Admin(Document):

    username = StringField(unique=True, required=True, error_message={
        'unique' : 'Username not available',
        'required': 'Username is required'
    })

    __password = StringField(required=True, error_message={
        'required': 'Password is required'
    })

    meta = {
        'collection': 'admins'
    }

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')