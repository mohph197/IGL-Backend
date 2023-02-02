from flask import request,jsonify
import sys
import requests
from bs4 import BeautifulSoup
import concurrent.futures
from app.admin.models import AnnouncementObj
from app.admin import annonces_algerie_url,get_auth_admin

def get_html(url):
    page = requests.get(url)
    return page.content

#Function to get all infos of a single announcement
def get_infos(link):
    soup = BeautifulSoup(get_html(link),"html.parser")
    announcement = AnnouncementObj()

    announcement.titre = soup.find(class_="da_entete").get_text()

    info_labels = soup.find_all(class_="da_label_field")
    info_items = soup.find_all(class_="da_field_text")
    
    for i in range(min(len(info_labels),len(info_items))):
        label = info_labels[i].get_text()
        info = info_items[i]
        if label == "Catégorie":
            categorie_items = info.find_all("a")
            announcement.categorie = categorie_items[1].get_text()
            announcement.type = categorie_items[2].get_text()
        elif label == "Localisation":
            localisation_items = info.find_all("a")
            announcement.wilaya = localisation_items[2].get_text()
            announcement.commune = localisation_items[3].get_text()
        elif label == "Adresse":
            announcement.adresse = info.get_text()
        elif label == "Surface":
            announcement.surface = float(info.get_text().replace(' ','').replace('m²',''))
        elif label == "Prix":
            announcement.prix = float(info.get_text().replace(' ','').replace('DinarAlgèrien(DA)',''))
        elif label == "Texte":
            announcement.description = info.get_text()
        elif label == "Insérée le":
            announcement.date_publication = info.get_text().replace('/','-')

    images = soup.find_all(class_="PhotoMin1")
    announcement.photos = []
    for image in images:
        announcement.photos.append(annonces_algerie_url+image['src'])
    
    return announcement.to_json()

def get_online():
    admin = get_auth_admin()
    if admin:
        page = '1'
        if 'page' in request.args:
            page = request.args.get('page')

        #Beginning of the script ================================================================================
        sub_url = "AnnoncesImmobilier.asp"

        if len(sys.argv) > 0:
            sub_url += "?rech_page_num="+str(sys.argv[0])

        try:
            soup = BeautifulSoup(get_html(annonces_algerie_url+sub_url), "html.parser")
            items = soup.find_all(class_="Tableau1")

            links = []
            for item in items:
                link = item.find_all("td")[7].find("a")["href"]
                links.append(annonces_algerie_url+link)

            # This part use multi-threading to optimise execution time
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = list(executor.map(get_infos, links))
            
            return jsonify({
                'annonces' : results,
                'page': page,
                'annonces_per_page': 25,
            }),200

        except Exception as e:
            return jsonify(
                {
                    'error': e.args,
                    'message': 'Error',
                }
            ),500
    else:
        return jsonify(
            {
                'error':'Unauthorized',
                'message':'Error',
            }
        ),403