import os
import scrapy

from scrapy.http import Request

class HinosCancoesEB(scrapy.Spider):
    """Spider to download military songs from Brazilian Army."""
    name = 'eb'

    def start_requests(self):
        yield Request('http://www.eb.mil.br/web/midia-eletronica/hinos-e-cancoes3_old')

    def parse(self, response):
        links = response.xpath('//td[@class="table-cell"]/a/@href').extract()
        for link in links:
            yield Request(
                    link,
                    callback=self.parse_musicas
                    )

    def parse_musicas(self, response):
        song = response.xpath('normalize-space(//h3[@class="header-title"]/span/text())').extract_first()
        filename = os.getcwd() + '/' + song + '.mp3'
        url = response.urljoin(response.xpath('//a[contains(.,"Baixe aqui")]/@href').extract_first())
        yield Request(
                url,
                meta={
                    "url": url,
                    "filename": filename,
                    "song": song,
                    },
                callback=self.parse_musica,
                )

    def parse_musica(self, response):
        yield {
                "song": response.meta["song"],
                "url": response.url,
                }
        with open(response.meta["filename"], 'wb') as f:
            f.write(response.body)
