"""
Defining Scrapers classes
Author: João Fonseca
Date: 16 July 2022
"""

from bs4 import BeautifulSoup as bsoup
from lxml import etree
import asyncio
import httpx



class OLXScraper:

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36 Edg/103.0.1264.62'}

    def __init__(self):
        pass

    async def get_pages_number(self,client,url):
        response = await client.get(url,headers=OLXScraper.header)
        print(response)
        soup = bsoup(response.content, "html.parser")
        parsed = etree.HTML(str(soup))
        max = parsed.xpath('/html/body/div[1]/div[1]/div[2]/form/div[5]/div/section[1]/div/ul/li[5]/a/@text')
        if max==[]:
            return 5
        else:
            print(max[0])
            return int(max[0])

    async def get_page_ads_urls(self,url,client):
        done,n = False,1
        urls = []
        response = await client.get(url,headers=OLXScraper.header)
        soup = bsoup(response.content, "html.parser")
        parsed = etree.HTML(str(soup))
        while not(done):
            div = parsed.xpath(f'/html/body/div[1]/div[1]/div[2]/form/div[5]/div/div[2]/div[{n}]')
            if div==[]:
                done = True
            else:
                pre_url = div[0].xpath('a/@href')
                if pre_url!=[]:
                    urls += [pre_url[0]]
            n+=1
        return urls 

    async def _async_get_ads(self,main_url):

        async with httpx.AsyncClient() as client:
            max_page = await self.get_pages_number(client,main_url)
            print(max_page)
            tasks = []
            for number in range(1, max_page):
                url = main_url+f'?page={number}'
                tasks.append(asyncio.ensure_future(get_page_ads_urls(url, client)))

            urls = await asyncio.gather(*tasks)
            return urls

    def get_all_ads_urls(self,main_url):
        urls_per_page = asyncio.run(self._async_get_ads(main_url))
        return [item for sublist in urls_per_page for item in sublist]


        




