from app import db

favorites = db.Table('favori',
    db.Column('annonce_id', db.Integer, db.ForeignKey('annonce.id')),
    db.Column('utilisateur_email', db.String(100), db.ForeignKey('utilisateur.email'))
)

class User(db.Model):
    __tablename__ = 'utilisateur'
    __table_args__ = {'extend_existing': True} 
    email = db.Column(db.String(100), primary_key=True, nullable=False)
    nom = db.Column(db.String(20), nullable=False)
    prenom = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(1),default='U',nullable=False)

    annonces_poste = db.relationship('Announcement', backref='auteur', lazy='dynamic')
    annonces_favoris = db.relationship('Announcement', secondary=favorites, backref='fans', lazy='dynamic')
    messages_envoyes = db.relationship('Message', backref='emetteur', lazy='dynamic', foreign_keys='Message.emetteur_email')
    messages_recus = db.relationship('Message', backref='destinataire', lazy='dynamic', foreign_keys='Message.destinataire_email')
    contact_info = db.relationship('ContactInfo', backref='utilisateur', uselist=False)

    def __repr__(self):
        return f'<User {self.email}>'

class Announcement(db.Model):
    __tablename__ = 'annonce'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    type = db.Column(db.Text)
    surface = db.Column(db.Float)
    description = db.Column(db.Text)
    prix = db.Column(db.Float, nullable=False)
    categorie = db.Column(db.Enum('Vente','Echange','Location','Location pour vacances'), nullable=False)
    
    auteur_email = db.Column(db.String(100), db.ForeignKey('utilisateur.email'), nullable=False)
    localisation_id = db.Column(db.Integer, db.ForeignKey('localisation.id'), nullable=False)
    contactinfo_email = db.Column(db.String(100), db.ForeignKey('contactinfo.email'), nullable=False)

    photos = db.relationship('Picture', backref='annonce', lazy='dynamic')

    def __repr__(self):
        return f'<Announcement {self.id}>'

class Location(db.Model):
    __tablename__ = 'localisation'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    wilaya = db.Column(db.String(100))
    commune = db.Column(db.String(100))
    adresse = db.Column(db.Text, nullable=False)

    annonces = db.relationship('Announcement', backref='localisation', lazy='dynamic')

    def __repr__(self):
        return f'<Location {self.id}>'

class ContactInfo(db.Model):
    __tablename__ = 'contactinfo'
    email = db.Column(db.String(100), db.ForeignKey('utilisateur.email'), primary_key=True, nullable=False)
    nom = db.Column(db.String(20), nullable=False)
    prenom = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    tel = db.Column(db.String(20))

    annonces = db.relationship('Announcement', backref='contactinfo', lazy='dynamic')

    def __repr__(self):
        return f'<ContactInfo {self.email}>'

class Picture(db.Model):
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nom = db.Column(db.Text, nullable=False)
    chemin = db.Column(db.Text, nullable=False)

    annonce_id = db.Column(db.Integer, db.ForeignKey('annonce.id'), nullable=False)

    def __repr__(self):
        return f'<Picture {self.id}>'

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    objet = db.Column(db.Text, nullable=False)
    contenu = db.Column(db.Text, nullable=False)

    emetteur_email = db.Column(db.String(100), db.ForeignKey('utilisateur.email'), nullable=False)
    destinataire_email = db.Column(db.String(100), db.ForeignKey('utilisateur.email'), nullable=False)

    def __repr__(self):
        return f'<Message {self.id}>'
