import requests
from bs4 import BeautifulSoup
import ast
import datetime


req = requests.get("https://deals.jumia.ci/abidjan/vehicules/")
link_statut = req.status_code
page = 1
print (page)

prix_eleve = 0
prix_bas = 0
poste = 0
	
hier = datetime.datetime.now() - datetime.timedelta(days=1)
def hierdate(date):
	global day

	day = ""

	date_object = datetime.datetime.strptime(date, '%d.%m.%Y %H:%M')
	
	day = date_object.date()

	return day


	
while link_statut == 200:
	page = BeautifulSoup(req.text, "lxml")
	for poste1 in page.findAll({'article'}):
			date = poste1.find('time').get('datetime')
			if hierdate(date) == hier.date():
				poste += 1
				price = float(ast.literal_eval(poste1.get('data-event'))['price'])

				marque_vt = poste1.find('a',{'class':'post-link post-vip'}).get('title')

				if int(price) > prix_eleve:
					prix_eleve = int(price)
					mark = marque_vt
				else:
					prix_bas = int(price)
					marque = marque_vt
	page += 1
	print (page)
	adresse = "https://deals.jumia.ci/abidjan/vehicules?page="+ str(page)

	req = requests.get(adresse)
	link_statut = req.status_code
	
	if page == 300:
		break

print ('Hier : ',hier.date())
print ('Il y a eu ', poste,' voiture(s) postee(s) sur jumia Deals')
print ('La voiture la plus chere etait une ',mark, 'elle vaut ',prix_eleve)
print ('La voiture la moins chere etait une ',marque, 'elle vaut ',prix_bas)
