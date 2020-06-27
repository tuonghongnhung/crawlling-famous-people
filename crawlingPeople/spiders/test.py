import scrapy
from ..items import CrawlingpeopleItem, ImageItem
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import shutil
import requests
import csv

def get_links_people():
    df = pd.read_excel("./tong hop link.xlsx")
    links = df['URL']
    links = links.tolist()
    link_people = filter(lambda link: "people" in link, links)
    link_people = filter(lambda link: "%" not in link, links)
    link_people = filter(lambda link: "html"  in link, links)
    
    return list(link_people)[:3]

class FamousPeople(scrapy.Spider):
    name = 'famous'
    allowed_domain = ['www.famousbirthdays.com']
    start_urls = get_links_people()
    
    def parse(self, response):
        data = CrawlingpeopleItem()
        data_resp = scrapy.Selector(response)
        tmp = {}

        name = data_resp.xpath("//*[@class = 'main-info']//h1//text()").extract_first()
        if name is None:
            name = data_resp.xpath("//*[@class = 'page-title']/text()").extract_first()
            
        if name is not None:
            name = name.replace('\n', '')
            tmp['name'] = name
            
            job = data_resp.xpath("//div[@class='person-title']//text()").extract()
            temp = ''
            temp = temp.join(job)
            job = temp 
            job = job.replace("\n","")
            tmp['job'] = job
            

            img = data_resp.xpath("//div[@class = 'famous-slider']//img/@src").extract_first()
            if img is None:
                img = data_resp.xpath("//img[@class = 'img-responsive']/@src").extract_first()

            if img is not None:
                filename = name
                if '.' in filename:
                    filename = filename.replace(".","")
                
                if " " in filename:
                    filename = filename.replace(" ","-")

                r = requests.get(img, stream = True)

                if r.status_code == 200:
                    r.raw.decode_content = True
                    with open("./image/" + filename + ".jpg",'wb') as f:
                        shutil.copyfileobj(r.raw, f)

                tmp['link'] = filename

            info = data_resp.xpath("//div[@class='row main-stats']//*[@class='stat box']//text()").extract()
            if len(info) == 0:
                info = data_resp.xpath("//div[@class='row main-stats ']//*[@class='stat box']//text()").extract()

            title = []
            for ind in range(len(info)):
                if 'BIRTHDAY' in info[ind].upper() or 'BIRTHPLACE' in info[ind].upper() or 'BIRTH SIGN' in info[ind].upper() or 'AGE' in info[ind].upper():
                    title.append(ind)
            title.append(len(info))
            
            for i in range(len(title)-1):
                temp = ''
                temp = temp.join(info[title[i] + 1: title[i+1]])
                temp = temp.replace("\n", "")
                temp = temp.replace(" ", "")
                tmp[info[title[i]]] = temp

            data['quick_info'] = tmp

            detail = {}
            detail_info = data_resp.xpath("//div[@class = 'container']//div[@class='row']//div[@class = 'bio col-sm-7 col-md-8 col-lg-6']//*//text()").extract()
            if len(detail_info) == 0:
                
                detail_info = data_resp.xpath("//*[@class = ' col-sm-5  group-about']//text()").extract()

            items = []
            for i in range(len(detail_info)):
                temp = detail_info[i]
                
                temp = temp.replace("\xa0","")
            
                detail_info[i] = temp

                if detail_info[i] == 'About' or detail_info[i] == 'Before Fame' or detail_info[i] == 'Trivia' or detail_info[i] == 'Family Life' or detail_info[i] == 'Associated With':
                    items.append(i)

            items.append(len(detail_info))

            for ind in range(len(items)-1):
                temp = ''
                temp = temp.join(detail_info[items[ind] + 1 : items[ind + 1]])
                temp = temp.replace('\n', '')
                detail[detail_info[items[ind]]] = temp

            data['detail_info'] = detail
            yield data

