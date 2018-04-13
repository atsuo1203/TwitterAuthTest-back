from flaskr import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    twitter_id = db.Column(db.Text)
    name = db.Column(db.Text)
    access_token = db.Column(db.Text)
    access_token_secret = db.Column(db.Text)

    def to_json(self):
        return {
            "id": self.id,
            "twitter_id": self.twitter_id,
            "name": self.name,
            "access_token": self.access_token,
            "access_token_secret": self.access_token_secret
        }

    def create(self, twitter_id: str, name: str,
               access_token: str, access_token_secret: str):
        self.twitter_id = twitter_id
        self.name = name
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        db.session.add(self)
        db.session.commit()

    def update(self, data: dict):
        if data.get('twitter_id') is not None:
            self.twitter_id = data.get('twitter_id')
        if data.get('name') is not None:
            self.name = data.get('name')
        if data.get('access_token') is not None:
            self.access_token = data.get('access_token')
        if data.get('access_token_secret') is not None:
            self.access_token = data.get('access_token_secret')
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


def init():
    db.create_all()
