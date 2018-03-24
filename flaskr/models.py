from flaskr import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)

    def __repr__(self):
        return '<User id={id} name={name!r}>'.format(
                id=self.id, name=self.name)


def init():
    db.create_all()
