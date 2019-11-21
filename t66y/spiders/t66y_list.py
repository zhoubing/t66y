import scrapy
from scrapy import Request


class T66yList(scrapy.Spider):
    name = 't66ylist'
    allowed_domains = ['t66y.com', 'filefab.com']

    def start_requests(self):
        index = 1
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
        print("" + str(posts))
        title = posts[5].xpath("td[@class='tal']//a/text()").extract_first()
        author = posts[5].xpath("td/a[@class='bl']/text()").extract_first()
        time = posts[5].xpath("td/a[@class='f10']/text()").extract_first()
        url = posts[5].xpath("td[@class='tal']//a/@href").extract_first()

        print(title)
        print(author)
        print(time)
        print(url)
        yield Request('http://t66y.com/' + url, callback=self.parse_detail,
                      dont_filter=True, meta={'proxy': 'http://127.0.0.1:1087'})

    def parse_detail(self, response):
        details = response.xpath("//div[@class='tpc_content do_not_catch']/text()")
        name = self.get_text(details, "名称")
        vformat = self.get_text(details, "格式")
        code = self.get_text(details, "编码")
        software = self.get_text(details, "软件")
        mosaic = self.get_text(details, "有碼無碼")
        available = self.get_text(details, "期限")

        print(name)
        print(vformat)
        print(code)
        print(software)
        print(mosaic)
        print(available)

        imgs = response.xpath("//div[@class='tpc_content do_not_catch']/img/@data-src")
        for img in imgs:
            print(img.extract())

        external_links = response.xpath("//span[@style='display:inline-block;color:#669900']/@text")
        for links in external_links:
            print(links)

    @staticmethod
    def get_text(li, value):
        for item in li:
            if value in item.extract():
                return item.extract()
        return ""
