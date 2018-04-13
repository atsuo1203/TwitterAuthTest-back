from flaskr import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    twitter_id = db.Column(db.Text)
    name = db.Column(db.Text)
    token = db.Column(db.Text)

    def to_json(self):
        return {
            "id": self.id,
            "twitter_id": self.twitter_id,
            "name": self.name,
            "token": self.token
        }

    def create(self, twitter_id: str, name: str, token: str):
        self.twitter_id = twitter_id
        self.name = name
        self.token = token
        db.session.add(self)
        db.session.commit()

    def update(self, data: dict):
        if data.get('twitter_id') is not None:
            self.twitter_id = data.get('twitter_id')
        if data.get('name') is not None:
            self.name = data.get('name')
        if data.get('token') is not None:
            self.token = data.get('token')
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


def init():
    db.create_all()
