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
        max = parsed.xpath('/html/body/div[1]/div[1]/div[2]/form/div[5]/div/section[1]/div/ul/li[5]/a')
        if max==[]:
            return 5
        else:
            return int(max[0].text)

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
            tasks = []
            for number in range(1, max_page):
                url = main_url+f'?page={number}'
                tasks.append(asyncio.ensure_future(self.get_page_ads_urls(url, client)))

            urls = await asyncio.gather(*tasks)
            return urls

    def get_all_ads_urls(self,main_url):
        urls_per_page = asyncio.run(self._async_get_ads(main_url))
        return [item for sublist in urls_per_page for item in sublist]


class CarOLXScraper(OLXScraper):

    base_url = 'https://www.olx.pt/d/carros-motos-e-barcos/carros/q-carros/'

    def __init__(self):
        pass

    def get_all_ads_filter(self, min_price=None, max_price=None, min_year=None, max_year=None,
        max_kms=None, ignore_out=True, asc_by_time=True):
        '''
        ignore_out: ignore ads that redirect to other sites (ex: Standvirtual)
        asc_by_time: finds recent ads in OLX
        '''
        url = self.base_url + '?'
        if min_price is not None:
            url += f'search%5Bfilter_float_price:from%5D={min_price}&'
        if max_price is not None:
            url += f'search%5Bfilter_float_price:to%5D={max_price}&'
        if min_year is not None:
            url += f'search%5Bfilter_float_year:from%5D={min_year}&'
        if max_year is not None:
            url += f'search%5Bfilter_float_year:to%5D={max_year}&'
        if max_kms is not None:
            url += f'search%5Bfilter_float_quilometros:to%5D={max_kms}&'
        if asc_by_time:
            url += f'search%5Border%5D=created_at:desc&'
        url = url[:-1]
        urls = self.get_all_ads_urls(url)
        if ignore_out:
            return list(filter(lambda x : x[:2]!='ht',urls))
        else:
            return urls

    def get_add_info(self,url,client):
        '''
        TODO: 
        1. filtros para descricoes
        ou nao
        2. decidir se criamos o cliente antes, ou se abrimos um novo quando vamos ver os urls
        
        '''
        pass





        




