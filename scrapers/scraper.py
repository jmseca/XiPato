"""
Defining Scrapers classes
Author: João Fonseca
Date: 16 July 2022
"""

from bs4 import BeautifulSoup as bsoup
from lxml import etree
import asyncio
import httpx

from .CarBrands import *
from .exceptions import *
from .Entities import *


class AdScraperWithPages:
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36 Edg/103.0.1264.62'}

    def __init__(self,lowest_page):
        self.lowest_page = lowest_page

    async def get_parsed(self,client,url):
        response = await client.get(url,headers=self.header)
        soup = bsoup(response.content, "html.parser")
        parsed = etree.HTML(str(soup))
        return parsed

    def get_xpath_element_text(self,parsed,xpath,exception,exception_info=None,ignore_failure=False):
        pre_el = parsed.xpath(xpath)
        if pre_el==[]:
            if ignore_failure:
                return None
            else:
                if exception_info is None:
                    raise exception()
                else:
                    raise exception(exception_info)
        else:
            return pre_el[0].text

    async def get_pages_number_core(self,client,url,page_num_xpath):
        parsed = await self.get_parsed(client,url)
        max = parsed.xpath(page_num_xpath)
        if max==[]:
            return self.lowest_page
        else:
            return int(max[0].text)


    async def get_page_ads_urls_core(self,url,client,main_xpath,sub_xpath):
        '''
        main_xpath has to follow the pattern below:
        (...)/div[n] -> div[n] is what chages, so, main_xpath has to be
        (...)/div
        '''
        done,n = False,1
        urls = []
        parsed = await self.get_parsed(client,url)
        while not(done):
            div = parsed.xpath(main_xpath+f'[{n}]')
            if div==[]:
                done = True
            else:
                pre_url = div[0].xpath(sub_xpath)
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

    async def _get_async_car_ads_info(self, urls, site, brand, model):
        size = len(urls)
        print(size)
        all_info = [CarAd(site)]*size
        async with httpx.AsyncClient() as client:
            i=0
            for url in urls:
                await self.get_ad_info(url,client,i,all_info, brand=brand, model=model)
                i+=1
        return all_info



class SVScraper(AdScraperWithPages):

    base_url = 'https://www.standvirtual.com/carros'

    def __init__(self):
        lowest_page = 5
        super().__init__(lowest_page)

    async def get_pages_number(self,client,url):
        return await self.get_pages_number_core(client,url,'/html/body/div[1]/div/div/div/div[1]/div[2]/div[2]/div[1]/div[3]/div[3]/div/ul/li[6]/a/span')

    async def get_page_ads_urls(self,url,client):
        return await self.get_page_ads_urls_core(url, client,
            '/html/body/div[1]/div/div/div/div[1]/div[2]/div[2]/div[1]/div[3]/main/article',
            'div[1]/h2/a/@href'
        )

    def get_ads_urls_by_car(self,car_brand,car_model,year,delta=2):
        main_url = self.base_url + f'/{car_brand}/{car_model}/'
        min_year, max_year = year-delta,year+delta
        main_url += f'desde-{min_year}?search%5Bfilter_float_first_registration_year%3Ato%5D={max_year}'
        return self.get_all_ads_urls(main_url)

    def get_price(self,parsed, url):
        pre_price = self.get_xpath_element_text(parsed,
        '/html/body/div[3]/main/div[1]/div[2]/div[1]/div[1]/div[2]/div/span[1]',
        NoPriceException,url)
        return int(pre_price.replace(' ',''))


    def get_kms(self,parsed, url):
        pre_kms = self.get_xpath_element_text(parsed,
        '/html/body/div[3]/main/div[1]/div[1]/div[2]/div[1]/div[1]/div[3]/div[1]/ul[1]/li[8]/div',
        NoKmsException,url)
        kms_split = pre_kms.split(' ')
        if kms_split[-1]!='km':
            raise NoKmsException(url)
        return int(''.join(kms_split[:-1]))

    def get_year(self,parsed,url):
        pre_year = self.get_xpath_element_text(parsed,
            '/html/body/div[3]/main/div[1]/div[1]/div[2]/div[1]/div[1]/div[3]/div[1]/ul[1]/li[7]/div',
            NoYearException,url)
        if len(pre_year)!=4 or not(pre_year.isdigit()):
            raise NoYearException
        return int(pre_year)

    def get_svcar_info(self, parsed, url):
        info = [None,None,None]
        try:
            #price
            info[0] = self.get_price(parsed,url)
            #kms
            info[1] = self.get_kms(parsed, url)
            #year
            info[2] = self.get_year(parsed, url)
        except:
            return []
        return info


    async def get_ad_info(self,url,client,i,info,brand,model):
        parsed = await self.get_parsed(client,url)
        info = self.get_svcar_info(parsed, url)
        if info!=[]:
            info[i].insert_info(brand,model,info[0],info[1],info[2],url)
        # If not all info is given, the ad is discarded (at least for now)


    def get_ads_info_by_car(self,car_brand,car_model,year,delta=2):
        brand = car_brand.lower().replace(' ','-')
        model = car_model.lower().replace(' ','-')
        urls = self.get_ads_urls_by_car(brand,model,year,delta=delta)
        info = asyncio.run(self._get_async_ads_info(urls,'sv',car_brand,car_model))


        



        



class OLXScraper(AdScraperWithPages):

    olx_url = 'https://www.olx.pt'

    def __init__(self):
        lowest_page = 5
        super().__init__(lowest_page)

    async def get_pages_number(self,client,url):
        return await self.get_pages_number_core(client,url,'/html/body/div[1]/div[1]/div[2]/form/div[5]/div/section[1]/div/ul/li[5]/a')

    def get_title(self, parsed, url):
        '''
        Returns the ad title
        '''
        return self.get_xpath_element_text(parsed,
            '/html/body/div[1]/div[1]/div[3]/div[3]/div[1]/div[2]/div[2]/h1',
            NoAdTitleException,exception_info=url
        )
    
    def get_price(self,parsed, url):
        return self.get_xpath_element_text(parsed,
        '/html/body/div[1]/div[1]/div[3]/div[3]/div[1]/div[2]/div[3]/h3/text()[1]',
        NoPriceException, exception_info=url)


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
        return await self.get_page_ads_urls_core(url, client,
            '/html/body/div[1]/div[1]/div[2]/form/div[5]/div/div[2]/div',
            'a/@href'
        )



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
        # lest element controls if all labels were given
        info = [None,None,None,0]
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
                info[3] = 1
                break
        return info


    async def get_ad_info(self,url,client,i,info,brand=None,model=None):
        parsed = await self.get_parsed(client,self.olx_url+url)
        try:
            brand = self.get_brand_from_title(parsed,url)
            price = self.get_price(parsed,url)
        except:
            # The ad gets discarded
            return
        labels_info = self.get_labels_info(parsed)
        if (labels_info[3]==1):
            info[i].insert_info(brand,labels_info[2],price,labels_info[0],labels_info[1],url)
        # If not all labels are given, the ad is discarded (at least for now)
        

    def get_ads_info(self, min_price=None, max_price=None, min_year=None, max_year=None,
    max_kms=None, ignore_out=True, asc_by_time=True):
        urls = self.get_all_ads_filter(min_price, max_price, min_year, max_year,
            max_kms, ignore_out, asc_by_time)
        info = asyncio.run(self._get_async_ads_info(urls,'olx',None,None))

        
        






        




