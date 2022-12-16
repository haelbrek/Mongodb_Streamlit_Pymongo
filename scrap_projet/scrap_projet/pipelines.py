# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class ScrapProjetPipeline:
    def process_item(self, item, spider):
        return item

class MovieScrapingPipeline:

    collection_name = "movies"

    def open_spider(self, spider):
        self.client = MongoClient("mongodb://localhost:27017")
        db = self.client["Scraping"]

        self.movie = db[self.collection_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.movie.insert_one(dict(item))
        return item