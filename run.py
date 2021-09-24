import datetime

from scrapy import cmdline

SPIDER = 'spider-name'

today = datetime.date.today()

if __name__ == '__main__':
    cmdline.execute(f'scrapy crawl {SPIDER} -O spider_name_{today}.json'.split())
