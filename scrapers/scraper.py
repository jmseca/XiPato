"""
Defining Scrapers classes
Author: João Fonseca
Date: 16 July 2022
"""

from bs4 import BeautifulSoup as bsoup
from lxml import etree
import asyncio
import httpx

from CarBrands import *
from Exceptions import *
from Entities import *



class OLXScraper:

    olx_url = 'https://www.olx.pt'
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

    def get_title(self, parsed, url):
        '''
        Returns the ad title
        '''
        #TODO: Criar excecao para quando nao ha titulo
        pre_title = parsed.xpath('/html/body/div[1]/div[1]/div[3]/div[3]/div[1]/div[2]/div[2]/h1')
        if pre_title==[]:
            #prolly does not have photo
            raise NoAdTitleException(url)
        else:
            return pre_title[0].text

    def get_labels(self,parsed):
        '''
        Gets the little labels tha exist in some of the ads.
        For example, in car ads, some of this labels indicate de Kms and the manufacturing year
        '''
        labels = []
        n=1
        done = False
        while not(done):
            elem = parsed.xpath(f'/html/body/div[1]/div[1]/div[3]/div[3]/div[1]/div[2]/ul/li[{n}]/p/span')
            if elem==[]:
                elem = parsed.xpath(f'/html/body/div[1]/div[1]/div[3]/div[3]/div[1]/div[2]/ul/li[{n}]/p')
                if elem==[]:
                    done = True
                    continue
            labels += [elem[0].text]
            n+=1
        return labels

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
        self.car_brands = CarBrands()

    def get_brand_from_title(self, parsed, url):
        try:
            title = self.get_title(parsed, url)
        except NoAdTitleException as e:
            return None
        words = title.split(' ')
        for word in words:
            if word.lower() in self.car_brands:
                return self.car_brands[word.lower()]
        raise NoCarBrandException(title)

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

    def get_labels_info(self,labels):
        '''
        Gets the info present in the labels. Returns the following:
        [Kms, Year, Car model]
        If a specific info is not provided, None is returned
        '''
        count = 0
        info = [None,None,None]
        for label in labels:
            if label[:5]=='Quilo':
                kms = label.split(' ')[1]
                info[0] = int(kms.replace('.',''))
                count+=1
            elif label[:3]=='Ano':
                info[1] = int(label.split(' ')[1])
                count+=1
            elif label[:6]=='Modelo':
                info[2] = label.split(' ')[1]
            if count==3:
                break
        return info


    async def get_ad_info(self,url,client,i,info):
        response = await client.get(self.olx_url+url,headers=OLXScraper.header)
        soup = bsoup(response.content, "html.parser")
        parsed = etree.HTML(str(soup))
        try:
            brand = self.get_brand_from_title(parsed,url)
        except NoCarBrandException as e:
            return
        labels_info = self.get_labels_info(parsed)
        info[i].insert_info(brand,labels_info[2],labels_info[0],url,labels_info[1])
        
    
    async def _get_async_ads_info(self, urls):
        size = len(urls)
        print(size)
        all_info = [CarAd('olx')]*size
        async with httpx.AsyncClient() as client:
            i=0
            for url in urls:
                print(i)
                await self.get_ad_info(url,client,i,all_info)
                i+=1
        return all_info

    def get_ads_info(self, min_price=None, max_price=None, min_year=None, max_year=None,
    max_kms=None, ignore_out=True, asc_by_time=True):
        urls = self.get_all_ads_filter(min_price, max_price, min_year, max_year,
            max_kms, ignore_out, asc_by_time)
        info = asyncio.run(self._get_async_ads_info(urls))

        
        






        




