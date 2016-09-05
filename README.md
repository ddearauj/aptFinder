# Apartment Search

The idea of this project is to create a group of crawlers to scrape apartament websites in order to find the best apartment given a set of preferences. The user will receive a message on Slack informing that a new apt matching the preferences has been found

## To-dos

There are a few things that must be done:

	Crawlers
	Google Maps API
	Database
	Slack Bot
	Website


### Crawlers

Pretty simple crawler with selenium to look through the website and get data such as:

    Price
    Location (address, city, state)
    rooms
    suits
    area
    parking spaces
    condominium
    tax
    number of floors
    building age
    is furnished?
    pool
    gym
    has ac?
    images
    telephone number
    coordinates

Websites crawled:

	Zap imoveis (done!)
	OLX


### Google Maps Api

Use the google maps api in order to find how far the apt is from the users' defined location
(for example, if the user wants to know how far the apt is from his work place and etc.)

### Database

Simple MySQL database using sqlalchemy containing the data from the crawler and from the google maps api

### Slack Bot

Use the slack api in order to inform the user of a new apt that matches the predefined preferences


## Would be a great add but not a priority

Get the image of the outside of the realty using google street view
Keep track of the prices per neighbourhood to look for trends and etc. and compare the apt with the avg