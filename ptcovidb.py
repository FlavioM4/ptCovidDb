from covid import Covid
from datetime import date
import sqlite3

connection = sqlite3.connect('covid_pt.db')
cursor = connection.cursor()
covid = Covid()
pt = covid.get_status_by_country_name('portugal')
toDate = date.today()

class CovidData:
	def __init__(self, confirmed, active, deaths, recovered):
		self.confirmed = confirmed
		self.active = active
		self.deaths = deaths
		self.recovered = recovered
	def displayNumbers(self):
		print("Portugal's TOTAL cases on the date of: ", toDate)
		print("Confirmed cases: ", self.confirmed)
		print("Active cases: ", self.active)
		print("Deaths: ", self.deaths)
		print("Recovered: ", self.recovered)

def printComparisons(sars, yestersars, cdif, adif, ddif, rdif, lastCheck):
	print("Todays confirmed cases: ", sars.confirmed, ". More ", cdif, " cases since ", lastCheck)
	if sars.active > yestersars.active:
		print("Todays active cases: ", sars.active, ". More ", adif, " active cases since ", lastCheck)
	else:
		print("Todays active cases: ", sars.active, ". Less ", adif, " active cases since ", lastCheck)
	print("Total deaths: ", sars.deaths, ". More ", ddif, " deaths since ", )
	print("Todays recovered: ", sars.recovered, ". More ", rdif, " recovered since ", lastCheck)


def compareNumbers(sars):
	yesterdata = cursor.execute("SELECT * FROM covidNumbers ORDER BY dateOf ASC LIMIT 1")
	dados = cursor.fetchone()
	lastCheck = dados[4]
	print(lastCheck)
	yestersars = CovidData(dados[0], dados[1], dados[2], dados[3])
	confDif = sars.confirmed - yestersars.confirmed
	actDif = sars.active - yestersars.active
	deaDif = sars.deaths - yestersars.deaths
	recoDif = sars.recovered - yestersars.recovered
	printComparisons(sars, yestersars, confDif, actDif, deaDif, recoDif,lastCheck)

def checkLastDay(sars):
	cursor.execute("SELECT * FROM covidNumbers")
	results = cursor.fetchall()
	if len(results) > 1:
		compareNumbers(sars)
	else:
		print("No previous day's data was found, can't compare.")
		sars.displayNumbers()


def checkDate(sars):
	today = str(toDate)
	cursor.execute("SELECT dateOf FROM covidNumbers WHERE dateOf=?", [today])
	result = cursor.fetchone()
	if result:
		checkLastDay(sars)
	else:
		dataEntry(sars)

def dataEntry(sars):
	confirmed, active, deaths, recovered = sars.confirmed, sars.active, sars.deaths, sars.recovered
	cursor.execute("INSERT INTO covidNumbers (confirmed, active, deaths, recovered, dateOf) VALUES (?, ?, ?, ?, ?)", (confirmed, active, deaths, recovered, toDate))
	checkLastDay(sars)

def createTable(sars):
	cursor.execute('CREATE TABLE IF NOT EXISTS covidNumbers(confirmed INTEGER, active INTEGER, deaths INTEGER, recovered INTEGER, dateOf TEXT)')
	dataEntry(sars)

def checkTable(sars):
	cursor.execute(f'SELECT count(name) FROM sqlite_master WHERE type="table" AND name="covidNumbers"')
	if cursor.fetchone()[0]==1:
		checkDate(sars)
	else:
		createTable(sars)

def checkNumbers():
	print("Today's date is ", toDate)
	data = {
		key: pt[key]
		for key in pt.keys() and {'confirmed' , 'active', 'deaths', 'recovered'}
	}

	sars = CovidData(data['confirmed'], data['active'], data['deaths'], data['recovered'])
	checkTable(sars)
	
def lastCheck():
	cursor.execute("SELECT")
checkNumbers()