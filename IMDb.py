import scrapy


class ImdbSpider(scrapy.Spider):
    name = 'IMDb'
    allowed_domains = ['-x']
    start_urls = ['http://-x/']

    def parse(self, response):
        pass
