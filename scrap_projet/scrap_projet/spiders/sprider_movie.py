# import scrapy

# class ImdbSpiderSpider(scrapy.Spider):
#     name = 'imdb_spider'
#     allowed_domains = ['imdb.com']
#     start_urls = ["https://www.imdb.com/search/title/?groups=top_250"]

    

    # def parse(self, response):

    #     movies = response.xpath("//div[@class='lister-item-content']")

    #     for movie in movies:
    #         movie_name = movie.xpath(".//h3//a//text()").get()  
    #         #movie_link = "https://www.imdb.com" + movie.xpath(".//h3//a//@href").get()
    #         movie_rating = movie.xpath(".//div[@class='ratings-bar']//strong//text()").getall()
    #         movie_genre = movie.xpath(".//span[@class='genre']//text()").getall()

    #         yield{
    #                 'movie name':movie_name,
    #                 #'movie link':movie_link,
    #                 'movie_rating':movie_rating,
    #                 'movie_genre':movie_genre,

    #               }

    # def parse(self,reponse):
    #      for link in reponse.css('span.lister-item-content')
# import scrapy
# class ImdbSpiderSpider(scrapy.Spider):
#     name = 'movies'
#     start_urls = ['https://www.imdb.com/chart/top/']
      
# def parse(self, response):
#     movieContent = response.css("td.titleColumn")
#     for item in movieContent:
#         movieName = item.css("a::text").get()
#         movieYear = item.css("span::text").get()
#         movieDict = {'Movie Name': movieName,
#                      'Release Year': movieYear}
#         yield movieDict
# import scrapy

# class ImdbSpider(scrapy.Spider):
#     name = 'imdb'
#     allowed_domains = ['www.imdb.com']
#     start_urls = ['http://www.imdb.com/']

# import scrapy

# class ImdbSpider(scrapy.Spider):
#     name = "imdb"
#     allowed_domains = ["imdb.com"]
#     start_urls = ['http://www.imdb.com/chart/top',]
   
#     def parse(self, response):
#         # table coloums of all the movies 
#         columns = response.css('table[data-caller-name="chart-top250movie"] tbody[class="lister-list"] tr')
#         for col in columns:
#             # Get the required text from element.
#             yield {
#                 # "id" : col.css("td[class='titleColumn'] :: text ").extract_first().strip(),
#                 "title": col.css("td[class='titleColumn'] a::text").extract_first(),
#                 "year": col.css("td[class='titleColumn'] span::text").extract_first().strip("() "),
#                 "rating": col.css("td[class='ratingColumn imdbRating'] strong::text").extract_first(),

#             }
# importing the scrapy
import scrapy
from  scrap_projet.items import MovieItem, CastItem

class ImdbSpider(scrapy.Spider):
    name = "imdb"
    allowed_domains = ["imdb.com"]
    base_url = "https://imdb.com"
    start_urls = ['https://www.imdb.com/chart/top',]
    handle_httpstatus_list = [403]
    custom_settings = {
    # spécifie l'ordre d'export des attributs de IMDBMovie (dans le CSV résultant par exemple)
    'FEED_EXPORT_FIELDS': ["title", "titre_original","genre",'public','years',"runtime", "rating_score","summary",'casting_principal'],
    }
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrap_projet.pipelines.MovieScrapingPipeline': 300
        }
        }


    def parse(self, response):
        # table coloums of all the movies 
        columns = response.css('table[data-caller-name="chart-top250movie"] tbody[class="lister-list"] tr')
        for col in columns:
            # rating of the movie i.e., position in the table
            rating = col.css("td[class='titleColumn']::text").extract_first().strip()
            # url of detail page of that movie. 
            rel_url = col.css("td[class='titleColumn'] a::attr('href')").extract_first().strip()
            # add the domain to rel. url
            col_url = self.base_url + rel_url
            # Make a request to above url, and call the parseDetailItem
            yield scrapy.Request(col_url, callback=self.parseDetailItem, meta={'rating' : rating})
    
    # calls every time, when the movie is fetched from table.
    def parseDetailItem(self, response):
        # create a object of movie.
        item = MovieItem()
        # fetch the rating meta.
        #item["rating"] = response.meta["rating"]
        # # Get the required text from element.
        item['rating_score'] = float(response.css('div[class="sc-7ab21ed2-2 kYEdvH"] span ::text ').extract_first().strip())
        item['title'] = response.css('div[class="sc-80d4314-1 fbQftq"] h1 ::text ').get().strip()
        item['titre_original'] = response.css('div[class="sc-dae4a1bc-0 gwBsXc"] ::text').get()
        item['years'] = response.css('li[class="ipc-inline-list__item"] span ::text').extract_first().strip()
        item['public'] = response.css('ul[class="ipc-inline-list ipc-inline-list--show-dividers sc-8c396aa2-0 kqWovI baseAlt"] li ::text').extract()[2].strip()
        item["summary"] = response.css('span[class="sc-16ede01-0 fMPjMP"]::text').extract_first().strip()

        item["genre"] = response.css('span[class="ipc-chip__text"] ::text').getall()[:-1]
        if len(response.css('li[class="ipc-inline-list__item"]::text').getall())>2 :
            item["runtime"] = int(response.css('li[class="ipc-inline-list__item"]::text').getall()[0])*60+int(response.css('li[class="ipc-inline-list__item"]::text').getall()[3])
        else : 
            if len(response.css('li[class="ipc-inline-list__item"]::text').getall()[0])==1 :
                item["runtime"] = int(response.css('li[class="ipc-inline-list__item"]::text').getall()[0])*60
            else :
                item["runtime"] = int(response.css('li[class="ipc-inline-list__item"]::text').getall()[0])
        item['pays']=response.xpath('/html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section/div[2]/ul/li[2]/div/ul/li/a/text').extract()

        item['casting_principal'] = response.css('a[class="sc-bfec09a1-1 gfeYgX"] ::text').extract()
        
        yield item 