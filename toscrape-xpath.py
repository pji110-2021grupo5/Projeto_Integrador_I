# -*- coding: utf-8 -*-
import scrapy


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-xpath'
    start_urls = [
        'http://www.camarasorocaba.sp.gov.br/materias.html',
    ]

    def parse(self, response):
        for quote in response.xpath('//ul[@class="pagination"]'):
            yield {
                'text': quote.xpath('./span[@class="materiaLegislativaTitle"]/text()').extract_first(),
                'author': quote.xpath('.//small[@class="text-danger sub-info materiaLegislativaInfo"]/text()').extract_first(),
                #'tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
            }

        next_page_url = response.xpath('//ul[@class="pagination"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

