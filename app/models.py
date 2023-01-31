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
    discussions_annonces = db.relationship('Discussion', backref='annonceur', lazy='dynamic', foreign_keys='Discussion.annonceur_email')
    discussions_demandees = db.relationship('Discussion', backref='demandeur', lazy='dynamic', foreign_keys='Discussion.demandeur_email')
    messages_envoyes = db.relationship('Message', backref='emetteur',lazy='dynamic')

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
            'discussions_annonces': [discussion.to_dict() for discussion in self.discussions_annonces],
            'discussions_demandees': [discussion.to_dict() for discussion in self.discussions_demandees],
        }

class Announcement(db.Model):
    __tablename__ = 'annonce'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    titre = db.Column(db.Text,nullable=False)
    type = db.Column(db.Text)
    surface = db.Column(db.Float)
    description = db.Column(db.Text)
    prix = db.Column(db.Float, nullable=False)
    adresse = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    categorie = db.Column(db.Enum('Vente','Echange','Location','Location pour vacances'), nullable=False)
    date_publication = db.Column(db.Date,nullable=False)
    
    auteur_email = db.Column(db.String(100), db.ForeignKey('utilisateur.email'), nullable=False)            # auteur
    localisation_id = db.Column(db.Integer, db.ForeignKey('localisation.id'), nullable=False)               # localisation

    photos = db.relationship('Picture', backref='annonce', lazy='dynamic')
    discussions = db.relationship('Discussion', backref='annonce',lazy='dynamic')

    def __repr__(self):
        return f'<Announcement {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'type': self.type,
            'surface': self.surface,
            'description': self.description,
            'prix': self.prix,
            'adresse': self.adresse,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'categorie': self.categorie,
            'date_publication': self.date_publication.strftime('%Y-%m-%d'),
        }

    def to_dict_with_relations(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'type': self.type,
            'surface': self.surface,
            'description': self.description,
            'prix': self.prix,
            'adresse': self.adresse,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'categorie': self.categorie,
            'date_publication': self.date_publication.strftime('%Y-%m-%d'),
            'auteur': self.auteur.to_dict(),
            'localisation': self.localisation.to_dict(),
            'photos': [photo.to_dict() for photo in self.photos],
            # 'discussions': [discussion.to_dict() for discussion in self.discussions]
        }

class Location(db.Model):
    __tablename__ = 'localisation'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    commune_name = db.Column(db.String(100))
    commune_name_ascii = db.Column(db.String(100),nullable=False)
    daira_name = db.Column(db.String(100))
    daira_name_ascii = db.Column(db.String(100),nullable=False)
    wilaya_code = db.Column(db.String(10))
    wilaya_name = db.Column(db.String(100))
    wilaya_name_ascii = db.Column(db.String(100),nullable=False)

    annonces = db.relationship('Announcement', backref='localisation', lazy='dynamic')

    def __repr__(self):
        return f'<Location {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'wilaya': self.wilaya_name_ascii,
            'wilaya_code': self.wilaya_code,
            'daira': self.daira_name_ascii,
            'commune': self.commune_name_ascii,
        }

    def to_dict_with_relations(self):
        return {
            'id': self.id,
            'wilaya': self.wilaya_name_ascii,
            'wilaya_code': self.wilaya_code,
            'daira': self.daira_name_ascii,
            'commune': self.commune_name_ascii,
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


class Discussion(db.Model):
    __tablename__ = 'discussion'
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    annonceur_email = db.Column(db.String(100), db.ForeignKey('utilisateur.email'), nullable=False)          # annonceur
    demandeur_email = db.Column(db.String(100), db.ForeignKey('utilisateur.email'), nullable=False)          # demandeur
    annonce_id = db.Column(db.Integer, db.ForeignKey('annonce.id'), nullable=False)                         # annonce

    messages = db.relationship('Message', backref='discussion', lazy='dynamic')

    def __repr__(self):
        return f'<Discussion {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'annonceur': self.annonceur_email,
            'demandeur': self.demandeur_email,
        }

    def to_dict_with_relations(self):
        return {
            'id': self.id,
            'annonceur': self.annonceur.to_dict(),
            'demandeur': self.demandeur.to_dict(),
            'annonce': self.annonce.to_dict(),
            'messages': [message.to_dict() for message in self.messages]
        }

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    objet = db.Column(db.Text, nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    lu = db.Column(db.Boolean, nullable=False)

    emetteur_email = db.Column(db.String(100), db.ForeignKey('utilisateur.email'), nullable=False)          # emetteur
    discussion_id = db.Column(db.Integer, db.ForeignKey('discussion.id'),nullable=False)                    # discussion
    
    def __repr__(self):
        return f'<Message {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'objet': self.objet,
            'contenu': self.contenu,
            'lu': self.lu,
            'emetteur': self.emetteur.to_dict(),
        }

    def to_dict_with_relations(self):
        return {
            'id': self.id,
            'objet': self.objet,
            'contenu': self.contenu,
            'lu': self.lu,
            'emetteur': self.emetteur.to_dict(),
            'discussion': self.discussion.to_dict()
        }
