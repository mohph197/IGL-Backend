from app import db

class User(db.Model):
    __tablename__ = 'utilisateur'
    email = db.Column(db.String(100), primary_key=True, nullable=False)
    nom = db.Column(db.String(20), nullable=False)
    prenom = db.Column(db.String(20), nullable=False)
    adresse = db.Column(db.Text)
    tel = db.Column(db.String(20))
    role = db.Column(db.String(1), default='U', nullable=False)

    annonces_poste = db.relationship('Announcement', backref='auteur', lazy='dynamic')
    messages_envoyes = db.relationship('Message', backref='emetteur', lazy='dynamic', foreign_keys='Message.emetteur_email')
    messages_recus = db.relationship('Message', backref='destinataire', lazy='dynamic', foreign_keys='Message.destinataire_email')

    def __repr__(self):
        return f'<User {self.email}>'

    def to_dict(self):
        return {
            'email': self.email,
            'nom': self.nom,
            'prenom': self.prenom,
            'adresse': self.adresse,
            'tel': self.tel,
            'role': self.role,
        }

    def to_dict_with_relations(self):
        return {
            'email': self.email,
            'nom': self.nom,
            'prenom': self.prenom,
            'adresse': self.adresse,
            'tel': self.tel,
            'role': self.role,
            'annonces_poste': [annonce.to_dict() for annonce in self.annonces_poste],
            'annonces_favoris': [annonce.to_dict() for annonce in self.annonces_favoris],
            'messages_envoyes': [message.to_dict() for message in self.messages_envoyes],
            'messages_recus': [message.to_dict() for message in self.messages_recus],
        }

class Announcement(db.Model):
    __tablename__ = 'annonce'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    type = db.Column(db.Text)
    surface = db.Column(db.Float)
    description = db.Column(db.Text)
    prix = db.Column(db.Float, nullable=False)
    categorie = db.Column(db.Enum('Vente','Echange','Location','Location pour vacances'), nullable=False)
    
    auteur_email = db.Column(db.String(100), db.ForeignKey('utilisateur.email'), nullable=False)            # auteur
    localisation_id = db.Column(db.Integer, db.ForeignKey('localisation.id'), nullable=False)               # localisation

    photos = db.relationship('Picture', backref='annonce', lazy='dynamic')
    messages = db.relationship('Message', backref='annonce', lazy='dynamic')

    def __repr__(self):
        return f'<Announcement {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'surface': self.surface,
            'description': self.description,
            'prix': self.prix,
            'categorie': self.categorie,
        }

    def to_dict_with_relations(self):
        return {
            'id': self.id,
            'type': self.type,
            'surface': self.surface,
            'description': self.description,
            'prix': self.prix,
            'categorie': self.categorie,
            'auteur': self.auteur.to_dict(),
            'localisation': self.localisation.to_dict(),
            'photos': [photo.to_dict() for photo in self.photos],
            'messages': [message.to_dict() for message in self.messages]
        }

class Location(db.Model):
    __tablename__ = 'localisation'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    wilaya = db.Column(db.String(100))
    commune = db.Column(db.String(100))
    adresse = db.Column(db.Text, nullable=False)

    annonces = db.relationship('Announcement', backref='localisation', lazy='dynamic')

    def __repr__(self):
        return f'<Location {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'wilaya': self.wilaya,
            'commune': self.commune,
            'adresse': self.adresse,
        }

    def to_dict_with_relations(self):
        return {
            'id': self.id,
            'wilaya': self.wilaya,
            'commune': self.commune,
            'adresse': self.adresse,
            'annonces': [annonce.to_dict() for annonce in self.annonces]
        }

class Picture(db.Model):
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nom = db.Column(db.Text, nullable=False)
    chemin = db.Column(db.Text, nullable=False)

    annonce_id = db.Column(db.Integer, db.ForeignKey('annonce.id'), nullable=False)     # annonce

    def __repr__(self):
        return f'<Picture {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'chemin': self.chemin,
        }

    def to_dict_with_relations(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'chemin': self.chemin,
            'annonce': self.annonce.to_dict()
        }

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    objet = db.Column(db.Text, nullable=False)
    contenu = db.Column(db.Text, nullable=False)

    emetteur_email = db.Column(db.String(100), db.ForeignKey('utilisateur.email'), nullable=False)          # emetteur
    destinataire_email = db.Column(db.String(100), db.ForeignKey('utilisateur.email'), nullable=False)      # destinataire
    annonce_id = db.Column(db.Integer, db.ForeignKey('annonce.id'), nullable=False)                         # annonce

    def __repr__(self):
        return f'<Message {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'objet': self.objet,
            'contenu': self.contenu,
        }

    def to_dict_with_relations(self):
        return {
            'id': self.id,
            'objet': self.objet,
            'contenu': self.contenu,
            'emetteur': self.emetteur.to_dict(),
            'destinataire': self.destinataire.to_dict(),
            'annonce': self.annonce.to_dict()
        }
