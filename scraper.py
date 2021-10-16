import scrapy

class CamaraSetSpider(scrapy.Spider):
    name = "Camaraset_spider"
    start_urls = ['http://www.camarasorocaba.sp.gov.br/materias.html']

    def parse(self, response):
        '''
        SET_SELECTOR = '.set'

        NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
        '''
        next_page = response.xpath("//a[@class='next_page']/@href").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
