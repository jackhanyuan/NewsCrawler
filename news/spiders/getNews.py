#! /usr/bin/python3
# coding=utf-8

import multiprocessing
from urllib.parse import urlparse
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.project import get_project_settings


class GetnewsSpider(CrawlSpider):
	name = 'getNews'
	allowed_domains = []
	start_urls = []

	def init(self, start_urls, allowed_domains):
		# super(TestSpider, self).__init__(*args, **kwargs)
		self.allowed_domains = allowed_domains
		self.start_urls = start_urls

	# self.allowed_domains = urlparse(start_urls).netloc
	# print(self.allowed_domains)

	'''
	@classmethod
	def GetnewsModify(cls, allowed_domains, start_urls):
		cls.allowed_domains = [allowed_domains]
		cls.start_urls = [start_urls]
		return cls
	'''

	# Rule(LinkExtractor(allow=r"https?://news\.cctv\.com/[0-9]{4}/[0-9]{2}/[0-9]{2}/.*?\.shtml.*?"), callback='parse_item', follow=True),
	rules = (
		Rule(LinkExtractor(allow=r"https?://.*?"), callback='parse_item', follow=True),
	)

	def parse_item(self, response):
		item = {}
		# item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
		# item['name'] = response.xpath('//div[@id="name"]').get()
		# item['description'] = response.xpath('//div[@id="description"]').get()
		if response.status == 200:
			url = response.url
			if url[-1] != '/':
				item['url'] = url
				if 'date' in response.headers:
					item['time'] = response.headers['date']
				yield item


def crawlers(url):
	# print(url)
	url_list = []
	domain = []
	crawler = CrawlerProcess(get_project_settings())
	url_list.append(url)
	domain.append(urlparse(url).netloc)
	crawler.crawl(GetnewsSpider, start_urls=url_list, allowed_domains=domain)
	crawler.start()


def processes(url_list, n):
	pool = multiprocessing.Pool(processes=n)
	for url in url_list:
		pool.apply_async(crawlers, (url,))
	pool.close()
	pool.join()


if __name__ == "__main__":
	# urls = [
	# 	"http://www.chinadaily.com.cn/"
	# ]
	urls = [
		"http://www.xinhuanet.com/",
		"https://www.huanqiu.com/",
		"https://news.qq.com/",
		"https://news.ifeng.com/",
		"http://www.chinanews.com/",
		"http://www.chinadaily.com.cn/"
	]
	processes(urls, len(urls))
