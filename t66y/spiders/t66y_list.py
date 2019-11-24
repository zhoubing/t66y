import scrapy
from scrapy import Request
import re


class T66yList(scrapy.Spider):
    name = 't66ylist'
    allowed_domains = ['t66y.com', 'filefab.com']

    def start_requests(self):
        for index in range(1, 101):
            yield Request('http://t66y.com/thread0806.php?fid=25&search=&page=' + str(index), callback=self.parse,
                          dont_filter=True, meta={'proxy': 'http://127.0.0.1:1087'})
        # yield Request('http://ip.filefab.com/index.php',
        #               callback=self.parse, dont_filter=True, meta={'proxy':'http://127.0.0.1:1087'})

    def parse(self, response):
        # ip = response.xpath("//h1[@id='ipd']/span/text()").extract_first()
        # print(ip)
        # country = response.xpath("//p[@id='cntdetected']/span/text()").extract_first()
        # print(country)
        posts = response.xpath("//tr[@class='tr3 t_one tac']")
        for index, post in enumerate(posts):
            title = post.xpath("td[@class='tal']//a/text()").extract_first()
            author = post.xpath("td/a[@class='bl']/text()").extract_first()
            time = post.xpath("td/a[@class='f10']/text()").extract_first()
            url = post.xpath("td[@class='tal']//a/@href").extract_first()
            if not url or len(re.split("[/.]", url)) < 4:
                continue
            symbols = re.split("[/.]", url)
            index = symbols[1] + symbols[2] + symbols[3]
            if url:
                yield Request('http://t66y.com/' + url, callback=self.parse_detail,
                              dont_filter=True,
                              meta={'proxy': 'http://127.0.0.1:1087',
                                    'item': {"title": title, "author": author, "time": time.strip(), "url": url, "index": int(index)}})
            else:
                print("url is none " + title)

    def parse_detail(self, response):
        details = response.xpath("//div[@class='tpc_content do_not_catch']/text()")
        print(details)
        name = self.get_text(details, "名稱")
        if not name:
            name = self.get_text(details, "名称")

        vformat = self.get_text(details, "格式")
        if not vformat:
            vformat = self.get_text(details, "格式")

        size = self.get_text(details, "大小")
        if not size:
            size = self.get_text(details, "大小")

        code = self.get_text(details, "编码")

        software = self.get_text(details, "軟件")
        if not software:
            software = self.get_text(details, "软件")

        mosaic = self.get_text(details, "有碼")
        if not mosaic:
            mosaic = self.get_text(details, "有码")

        available = self.get_text(details, "期限")
        if not available:
            available = self.get_text(details, "期限")

        item = response.meta['item']
        imgs = []
        detail_imgs = response.xpath("//div[@class='tpc_content do_not_catch']//img/@data-src")
        for img in detail_imgs:
            imgs.append(img.extract())

        links = []
        external_links = response.xpath("//a[@style='cursor:pointer;color:#2f5fa1;']")
        for link in external_links:
            links.append({
                "name": link.xpath("span//text()").extract_first(),
                "link": link.xpath("@href").extract_first()
            })

        item['detail'] = {
            "name": name,
            "vformat": vformat,
            "code": code,
            "software": software,
            "mosaic": mosaic,
            "available": available,
            "size": size,
            "imgs": imgs,
            "links": links
        }
        print(item)
        yield item

    @staticmethod
    def get_text(li, value):
        for item in li:
            if value in item.extract():
                return item.extract()
        return ""
