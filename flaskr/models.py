from flaskr import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    token = db.Column(db.Text)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "token": self.token
        }


def init():
    db.create_all()
