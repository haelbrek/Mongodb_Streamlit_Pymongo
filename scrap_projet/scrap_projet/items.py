# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# import scrapy


# class ScrapProjetItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass


# import scrapy

# class ImdbItem(scrapy.Item):
#     title = scrapy.Field()
#     directors = scrapy.Field()
#     writers = scrapy.Field()
#     stars = scrapy.Field()
#     popularity = scrapy.Field()
#     rating = scrapy.Field()

import scrapy

class MovieItem(scrapy.Item):
    title = scrapy.Field()
    titre_original=scrapy.Field()
    years=scrapy.Field()
    rating = scrapy.Field()
    summary = scrapy.Field()
    genre = scrapy.Field()
    runtime = scrapy.Field()
    #directors = scrapy.Field()
    #writers = scrapy.Field()
    #cast = scrapy.Field()
    rating_score=scrapy.Field()
    public=scrapy.Field()
    casting_principal=scrapy.Field()
    pays=scrapy.Field()

class CastItem(scrapy.Item):
    name = scrapy.Field()
    character = scrapy.Field()