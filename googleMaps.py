import settings
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib.error
import contextlib
import json

def getTimeDistance(placeA, placeB):
	"""
	uses the google maps API to get the distance and estimated time from A to B
	The input must be a dict with lat and lng. Lat being the latitude and lng the longitude
	
	"""

	url = ('https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + placeA['lat'] + ',' + placeA['lng'] + '&destinations=' + placeB['lat'] + ',' + placeB['lng'] + '&key=' + settings.MAPS_DIST_KEY)

	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	response = urlopen(req)
	jsobj = response.read().decode("utf-8")
	dic = json.loads(jsobj)

	return dic


apt = {'lat' : '-23.5656662458', 'lng' : '-46.653087045'}

getTimeDistance(apt, settings.IBM_COORD)