import json

import scrapy

extracted_data = []


def write_to_json(filename, data):
    f = open(filename, 'w')
    f.write(json.dumps(data))
    f.close()


class ApiScrollSpider(scrapy.Spider):
    name = 'api_scroll'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/api/quotes?page=1']

    def parse(self, response):
        r = json.loads(response.body)
        quotes = r.get('quotes')
        for q in quotes:
            nxdata = {
                'name': q.get('author').get('name'),
                'tags': q.get('tags'),
                'quotes': q.get('text')
            }
            extracted_data.append(nxdata)

        hn = r.get('has_next')
        if hn:
            next_page = r.get('page') + 1
            self.logger.info('scraping next page..')
            yield scrapy.Request(
                url=f'http://quotes.toscrape.com/api/quotes?page={next_page}',
                callback=self.parse
            )
        write_to_json('ext_data.json', extracted_data)
