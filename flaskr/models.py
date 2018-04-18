from flaskr import db


class User(db.Model):
    __tablename__ = 'users'
    twitter_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    access_token = db.Column(db.Text)
    access_token_secret = db.Column(db.Text)

    def __init__(self, twitter_id: int, name: str,
                 access_token: str, access_token_secret: str):
        self.twitter_id = twitter_id
        self.name = name
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def to_json(self):
        return {
            "twitter_id": self.twitter_id,
            "name": self.name,
            "access_token": self.access_token,
            "access_token_secret": self.access_token_secret
        }


def init():
    db.create_all()
