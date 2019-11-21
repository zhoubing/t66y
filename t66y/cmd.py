from scrapy import cmdline

cmdline.execute('scrapy runspider spiders/t66y_list.py -s JOBDIR=crawls/spider-1 -L WARNING'.split())
