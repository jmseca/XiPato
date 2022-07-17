"""
Defining Scrapers classes
Author: João Fonseca
Date: 16 July 2022
"""

import requests
from bs4 import BeautifulSoup as bsoup
from lxml import etree


class BsScraper:
    '''
    Scraper using bs4 library
    '''


class OLXScraper(BsScraper):

    def __init__(self):
        pass

    async def get_page_ads_urls(self,url,client):
        done = False
        n = 2
        urls = []
        while not(done):
            pre_url = await client.get(url)

            n+=1



    async def get_all_ads(self,**filters):

