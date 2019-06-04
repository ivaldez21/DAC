import scrapy


class JeansSpider(scrapy.Spider):
    name = "jeans"
    allowed_domains = ['obozrevatel.com', 'segodnya.ua', '24tv.ua', 'tsn.ua',
                      'strana.ua', 'pravda.com.ua', 'rbc.ua', 'unian.com',
                      'gordonua.com', 'nv.ua', 'liga.net', 'censor.net.ua',
                      'censor.net', '112.ua', 'korrespondent.net', 'unian.ua',
                      'unian.net', 'imi.org.ua', 'znaj.ua', 'ukranews.com',
                      'politeka.net', 'interfax.com.ua', 'apostrophe.ua',
                      'unn.com.ua', 'bagnet.org', 'kp.ua',
                     ]

    start_urls = [
        f'https://imi.org.ua/monitoring-types/doslidzhennya-dzhynsy/page/{i}/'
        for i in range(1, 2)
    ]

    # This is the parse function that is called from the landing page
    # so it only needs to return the htmls, it does not need other info
    def parse(self, response):
        for href in response.css('article a::attr(href)'):
            yield scrapy.Request(href.extract(), callback = self.parse_first)

    # This is the parse function for each artcile on the imi site. We are
    # not scraping the content, just the links to the other newsites
    def parse_first(self, response):
        for href in response.css('div.inner__container a::attr(href)'):
            yield scrapy.Request(href.extract(), callback = self.parse_second)

    # This is the parse function for the final level (first level links
    # from other sites within allowed_domains), and we scrape the link and html
    def parse_second(self, response):
        yield {
            'link': response.request.url,
            'html': response.text
        }
