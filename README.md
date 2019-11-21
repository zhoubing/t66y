# t66y
t66y spider

如果需要翻墙的话记得将setting中的robots关闭。因为开启的话框架会在爬虫请求之前去请求此网站的robots.txt文件，这个请求是不挂代理的，
开启他有可能造成后续请求延迟。ROBOTSTXT_OBEY = False
