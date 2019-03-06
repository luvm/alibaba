import requests
from lxml import etree
import os
import multiprocessing
import csv

address = os.path.abspath(os.path.dirname(__file__))
os.chdir(address)

class alibaba_Spider:
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"}
        self.page = "https://www.alibaba.com/products/camera.html?"
        self.name = 'name'
        self.proxies = {'http':'115.239.24.73'}
    def getPageUrl(self,params):
        res = requests.get(self.page.replace('camera',self.name),params=params,headers=self.headers)
        html = res.content
        parsehtml = etree.HTML(html)
        r_list = parsehtml.xpath('//h2[@class="title"]/a/@href')
        li = []
        for t_url in r_list:
            url = 'https:'+t_url
            li.append(url)
        ps = multiprocessing.Pool(8)
        ps.map(self.get_content, li)
        ps.close()
        ps.join()

    def get_content(self,t_url):
        try:
            s = requests.session()
            s.keep_alive = False

            res = requests.get(t_url,headers=self.headers)
            html = res.content
            parseHtml = etree.HTML(html)
            title = parseHtml.xpath('//*[@id="J-ls-grid-action"]/div[2]/div/div[1]/div/div[1]/h1/@title')[0]

            title = title.replace('/',' ').replace('*','x').replace(':',' ').replace('"',' ')

            main_list = parseHtml.xpath('//ul[@class="inav util-clearfix"]/li/div/a/img/@src')
            detail_list = parseHtml.xpath('//*[@id="J-rich-text-description"]//img/@src')
            for n,i in enumerate(main_list):
                try:
                    os.makedirs(os.path.join(address, self.name) + "\{}\{}".format(title, 'main'))
                except:
                    pass
                if i[:4] != 'http':
                    i = 'https:'+i.replace('50x50','350x350')
                print(i)
                self.writeImage(n=n,i=i,filename=title,type="main")
            for n,i in enumerate(detail_list):
                try:
                    os.makedirs(os.path.join(address, self.name) + "\{}\{}".format(title, 'detail'))
                except:
                    pass
                if i[:4] != 'http':
                    i = 'https:'+i
                print(i)
        except:
            print('t_url')


    def csv_writer(self,filename,video_url):
        print('写入视频链接')
        with open(os.path.join(address, self.name) + '.csv', 'at', newline='', encoding='gbk') as f:
            writer = csv.writer(f)
            writer.writerow((filename, video_url))

    def workOn(self):
        name = input("请输入商品名：")
        self.name = name
        begin = int(input("起始页："))
        end = int(input("终止页："))
        for page in range(begin, end + 1):
            params = {
                "page": str(page)
            }
            self.getPageUrl(params)


if __name__== "__main__":
    spider = alibaba_Spider()
    spider.workOn()



