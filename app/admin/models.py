def format_date(date):
        parts = date.split('-')
        return '-'.join(parts[::-1])

class AnnouncementObj:
    titre = None
    type = None
    surface = None
    description = None
    prix = 0
    wilaya = ''
    commune = ''
    adresse = ''
    categorie = 'Vente'
    date_publication = '0000-00-00'
    photos = []

    def __repr__(self):
        return '<Announcement Obj>'

    def to_json(self):
        return {
            'titre': self.titre,
            'type': self.type,
            'surface': self.surface,
            'description': self.description,
            'prix': self.prix,
            'wilaya': self.wilaya,
            'commune': self.commune,
            'adresse': self.adresse,
            'categorie': self.categorie,
            'date_publication': format_date(self.date_publication),
            'photos': self.photos,
        }