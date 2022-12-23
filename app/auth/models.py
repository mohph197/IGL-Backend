from app import db

class User(db.Model):
    __tablename__ = 'utilisateur'
    email = db.Column(db.String(100), primary_key=True, nullable=False)
    nom = db.Column(db.String(20), nullable=False)
    prenom = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(1),default='U',nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email