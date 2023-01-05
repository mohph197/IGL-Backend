import requests
from bs4 import BeautifulSoup
import concurrent.futures

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
    
    for info in info_labels:
        print(info)
    # categorie_items = info_items[0].find_all("a")
    # localisation_items = info_items[1].find_all("a")
    # surface_item = info_items[2]
    # prix_item = info_items[3]
    # description_item = info_items[4]
    # date_item = info_items[5]

    # announcement.categorie = categorie_items[1].get_text()
    # announcement.type = categorie_items[2].get_text()
    # announcement.wilaya = localisation_items[2].get_text()
    # announcement.commune = localisation_items[3].get_text()
    # announcement.adresse = localisation_items[3].get_text()




url = "http://www.annonce-algerie.com/"
sub_url = "AnnoncesImmobilier.asp"

soup = BeautifulSoup(get_html(url+sub_url), "html.parser")
items = soup.find_all(class_="Tableau1")
print(len(items))

links = []
for item in items:
    link = item.find_all("td")[7].find("a")["href"]
    links.append(url+link)
    get_infos(url+link)

# with concurrent.futures.ThreadPoolExecutor() as executor:
#     details_query = list(executor.map(get_infos, links))

# links = []
# infos = []
# #iterate in products
# cpt = 0
# for item in items:
#     try:
#         id_link = "https://www.auchan.fr"+item.find(class_="product-thumbnail__details-wrapper")["href"]
#         img_wrapper = item.find(class_="product-thumbnail__picture")
#         img_elem = img_wrapper.find("img")
#         image = ""
#         if 'srcset' in img_elem.attrs:
#             image = img_elem['srcset']
#         elif 'data-srcset' in img_elem.attrs:
#             image = img_elem['data-srcset']
#         name = item.find(class_='product-thumbnail__description').text
#         price = "NULL"
#         if not(all_products):
#             price = item.find(class_='product-price').text
#         cpt+=1
#         infos.append([name.replace('\n','').replace('\t',''), image, price])
#         links.append(id_link)
#     except:
#         pass


    
# print(len(details_query),len(infos),len(links))
# for i in range(0, len(details_query)):
#     infos[i].append(details_query[i][0])
#     infos[i].append(details_query[i][1][0])

# data += infos