# Created By : prongs7
# Parse Educational NGO's from http://ngo.india.gov.in/ngo_sector_ngo.php

import urllib3
from bs4 import BeautifulSoup
import requests
import numpy as np
from pandas import DataFrame
import openpyxl

def getNGOIds(noOfPages):
	http = urllib3.PoolManager()

	NGOids = []

	for i in range(1,noOfPages+1):
		r = http.request('GET', 'http://ngo.india.gov.in/sector_ngolist_ngo.php?page='+str(i)+'&psid=EDU')
		pos = r.data.find("</html>")
		data = r.data[177:]
		soup=BeautifulSoup(data)
		print("Loading NGO Ids of page : "+str(i))
		for link in soup.find_all('a'):
		    if(link.get('href').find("view_ngo")!=-1):
		    	temp = link.get('href')[21:]
		    	pos = temp.find("'")
		    	temp = temp[:pos]
		    	NGOids.append(temp)

	npIds = np.array(NGOids)
	np.save('top'+str(noOfPages*10)+'NGOIds', npIds)

def getNGOData(noOfNGOs):
	http = urllib3.PoolManager()

	NGOIds = np.load('top'+str(noOfNGOs)+'NGOIds.npy')

	nameNGOS = []
	cheifFunctionarys = []
	chairmans = []
	telephones = []
	mobiles = []
	emails = []
	addresses = []

	for i in range(len(NGOIds)):
		print("Getting NGO No : "+str(i))
		r = http.request('GET', 'http://ngo.india.gov.in/view_ngo_details_ngo.php?ngo_id='+NGOIds[i]+'&page_no=1')
		pos = r.data.find("</html>")
		data = r.data[177:]
		soup=BeautifulSoup(data)

		table1 = soup.find("table",cellpadding="5")
		rows = table1.find_all("tr")
		nameNGO = ""
		cheifFunctionary = ""
		chairman = ""
		telephone = ""
		mobile = ""
		email = ""

		for row in rows:
			cells = row.find_all("td")

			if(len(cells) >= 4):
				if(cells[1].get_text().find("Chairman")!=-1):
					chairman = cells[3].get_text()

				if(cells[1].get_text().find("Chief Functionary")!=-1):
					cheifFunctionary = cells[3].get_text()

				if(cells[1].get_text().find("Telephone")!=-1):
					telephone = cells[3].get_text()

				if(cells[1].get_text().find("Mobile No")!=-1):
					mobile = cells[3].get_text()

				if(cells[1].get_text().find("E-mail")!=-1):
					email = cells[3].get_text()

				if(cells[1].get_text().find("Address")!=-1):
					address = cells[3].get_text()

			for cell in cells:
				content = cell.get_text().encode('utf-8')
				if(content.find("NGO Name")!=-1):
					nameNGO = content

		nameNGO = nameNGO[11:]
		nameNGOS.append(nameNGO.strip())
		chairmans.append(chairman.strip())
		cheifFunctionarys.append(cheifFunctionary.strip())
		telephones.append(telephone.strip())
		mobiles.append(mobile.strip())
		emails.append(email.strip())
		addresses.append(address.strip())

	df = DataFrame({'NGO Name': nameNGOS, 'Chairman': chairmans,"Cheif Functionary": cheifFunctionarys, "Telephone" : telephones,"Mobile":mobiles,"EMail": emails,"Address": addresses})

	df.to_excel('NGO Data 1000.xlsx', sheet_name='sheet1', index=False)

#Enter number of NGO's in multiple of 10
noOfNGOs = 1000

#getNGOIds(noOfNGOs/10)
getNGOData(noOfNGOs)

