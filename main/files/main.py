from bots.bot import *
from psql.XiPatoDB import *
from scrapers.scraper import *

Bot = XiPatoBot('PLACE_BOT_ID_HERE',5464332087)
DB_Client = XiPatoUser('db.tecnico.ulisboa.pt','ist195749','PLACE_DB_PASSWD_HERE')
OLX_Scraper = OLXScraper()
SV_Scraper = SVScraper()
