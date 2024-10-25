from . import Document,StringField,ListField,IntField,ObjectIdField,FloatField,DateTimeField,datetime,signals

class Game(Document):

    gameName = StringField(unique=True, required=True, error_message={
        'unique' : 'Game not available',
        'required': 'Game name is required'
    })

    gameDescription = StringField(required=True, error_message={
        'required': 'Game description is required'
    })

    gameCategory = ListField(StringField())

    fileHash = StringField(required=True, unique=True, error_message={
        'unique' : 'Duplicate file detected',
        'required': 'Game hash is required'
    })

    gameKeywords = ListField(StringField())

    noOfLikes = IntField(default=0, min_value=0)

    noOfVotes = IntField(default=0, min_value=0)

    avgRating = FloatField(default=0,min_value=0,max_value=5)

    image = ObjectIdField()

    gamePath = ObjectIdField()  # Corresponds to "gamePath"

    gameType = StringField()

    releasedOn = DateTimeField(default=datetime.now())  # Corresponds to "createdAt"

    releasedBy = StringField(required=True, error_message={
        'required': 'Uploader username is required'
    })

    meta = {
        'collection':'games'
    }

    # Pre save processing
    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.gameName = document.gameName.lower()
        document.gameKeywords = [_.lower() for _ in document.gameKeywords]
        document.gameCategory = [_.lower() for _ in document.gameCategory]
        if document.noOfVotes > 0:
            document.avgRating = round(5 * (document.noOfLikes / document.noOfVotes), 1)
        else:
            document.avgRating = 0

    def to_dict(self):
        return {
            'gameName': self.gameName,
            'gameDescription': self.gameDescription,
            'gameCategory': self.gameCategory,
            'gamePath': str(self.gamePath),
            'image':str(self.image),
            'gameType': self.gameType,
            'releasedOn': self.releasedOn,
            'avgRating': self.avgRating,
            'noOfVotes': self.noOfVotes
        }

signals.pre_save.connect(Game.pre_save,sender=Game)
