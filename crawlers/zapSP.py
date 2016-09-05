# crawler para zap Imóveis em SP
# http://www.zapimoveis.com.br/aluguel/apartamentos/sp+sao-paulo/

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
import time

def getAddress(soup):
	"Returns dict with street, neighborhood, city and state of the apt/house"

	div = soup.find('div', {'class' : 'box-default clearfix endereco-imovel'})
	data = {}

	data.update(street = div.find('h1').text)

	data.update(loc = div.find('span', {'class' : 'logradouro'})) #format is neighborhood, city - State

	data.update(neighborhood = loc.partition(',')[0])
	data.update(city = loc.partition(',')[1].partition(" - ")[0])
	data.update(state = city = loc.partition(',')[1].partition(" - ")[1])

	return data

def getPrice(soup):
	"Returns the apt price"

	div = soup.find('div', {'class' : 'posvalue-imovel pull-right'})

	price = div.find('span', {'class' : 'value-ficha'}).text
	price = price.partition(" ")[1]

	if ("." in price):
		price = price.replace(".", "")

	return int(price)

def getRealtyInfo(soup):
	"Returns #rooms, #suits, size, #parkingSpaces"

	info = soup.find('div', {'class' : 'box-default clearfix informacoes-imovel'})
	sizeInfo = info.find('div', {'class' : 'pull-left'}).find('ul')
	taxInfo = info.find('div', {'class' : 'pull-right'}).find('ul')

	data = {}

	rooms = 0
	suits = 0
	size = 0
	parkingSpaces = 0

	for item in sizeInfo.findAll('li'):
		if (item.find('span').text == 'quarto'):
			rooms = int(item.text)
		elif (item.find('span').text == 'suíte'):
			suits = int(item.text)
		elif (item.find('span').text == 'Área Útil (m²)'):
			size = int(item.text)
		elif (item.find('span').text == 'vaga'):
			parkingSpaces = int(item.text)

	condo = 0
	iptu = 0

	for item in taxInfo.findAll('li'):
		if(item.find('span').text == 'Condomínio'):
			condo = item.text.partition(" ")[1]
			if("." in condo):
				condo = condo.replace(".", "")
			condo = int(condo)
		elif(item.find('span').text == 'IPTU'):
			iptu = item.text.partition(" ")[1]
			if("." in iptu):
				iptu = iptu.replace(".", "")
			iptu = int(iptu)

	data.update(
		rooms = rooms,
		suits = suits,
		size = size,
		parkingSpaces = parkingSpaces,
		condo = condo,
		iptu = iptu
	)

	return data

def getPhoneNumber(driver):
	"returns the phone number as a string"

	#we must click on the phone button in order for it to show on the page
	showPhoneButton = driver.find_element_by_class_name('icone-telefone btn-zap btn')

	ActionChains(driver).move_to_element(showPhoneButton).click(showPhoneButton).perform()

	soup = BeautifulSoup(driver.page_source, "lxml")

	phoneNumber = soup.find('span', {'class' : 'telefone'}).text

	return phoneNumber


def getCoordinates(soup):
	"Returns a dict with the latitude and longitude"

	div = soup.find('div', {'id' : 'imgMapaGoogleEstatico'})

	coord = div['onclick'] #on the format: funcname(lat, long, onclick)
	coord = coord.partition("(")[2] # lat, long, onclick)
	lat = coord.partition(",")[0]
	longi = coord.partition(",")[2].partition(",")[0]

	data = {}
	data.update(
		lat = lat,
		lng = longi
	)

	return data


#create a list with possible spellings and miss-spellings for each item. 
#In the future, use a fuzzy string match (fuzzywuzzy is a great lib for that)
ac = ['Ar Condicionado', 'Ár Condicionado', 'AR CONDICIONADO', 'ÁR CONDICIONADO']
pool = ['Piscina', 'Picina', 'Pissina']
gym = ['Academia', 'Ginástica', 'Ginastica']
party = ['Salão de Festas', 'Salao de Festas']
furnished = ['Mobilhado']
varanda = ['Varanda']


def getAdditionalInfo(soup):
	""" 
		gets the apt description and looks for the following info:
		#ofFloors
		constructionYear
		hasPool
		hasGym
		hasAc
		isFurnished
		hasPartyRoom (?)
		varanda (?)
	"""

	infos = soup.find('div', {'id' : 'caracteristicaOferta'})
	for idx, p in enumerate(infos.findAll('p')):
		if (idx == 0):
			floors = int(p.text[9:10])
			constructionYear = int(p.text.replace(" ", "")[-4:])
		if (idx == 1):
			hasAC = any(x in p.text for x in ac)
			isFurnished = any(x in p.text for x in furnished)
			hasVaranda = any(x in p.text for x in varanda)
		if (idx == 2):
			hasPool = any(x in p.text for x in pool)
			hasGym = any(x in p.text for x in gym)
			hasPartyRoom = any(x in p.text for x in party)

	data = {}
	data.update(
		floors = floors,
		constructionYear = constructionYear,
		hasAC = hasAC,
		isFurnished = isFurnished,
		hasVaranda = hasVaranda,
		hasPool = hasPool,
		hasGym = hasGym,
		hasPartyRoom = hasPartyRoom
	)

	return data


def getAptInfo(driver, soup):
	"Returns a dictionary with all the apt info"
	aptInfo = {}
	aptInfo.update(getAddress(soup))
	aptInfo.update(getPrice(soup))
	aptInfo.update(getRealtyInfo(soup))
	aptInfo.update(getPhoneNumber(driver))
	aptInfo.update(getCoordinates(soup))
	aptInfo.update(getAdditionalInfo(soup))

	return aptInfo



def scrapeZap(driver, soup):
	"returns a list with the apt info. In the future it will insert into the db the new offers and flag them to be sent by the slackBot"

	lastpage = False
	apartaments = []
	links = []

	#get all the links listed in the city so we can access each apt later
	while (!lastpage):
		for apts in soup.findAll('div', {'class' : 'list-cell'}):
			links.append(infos['href'])
		try:
			nextButton = driver.find_element_by_id('proximaPagina')
		except NoSuchElementException:
			print ('last page reached')
			lastPage = True
		else:
			nextButton = driver.find_element_by_id('proximaPagina')
			ActionChains(driver).move_to_element(nextButton).click(nextButton).perform()
			time.sleep(5)
	

	#get each individual apt info and ads it to the list apartments
	for link in links:
		driver.get(link)
		soup = BeautifulSoup(driver.page_source, "lxml")
		apartaments.append(getAptInfo(driver, soup))







