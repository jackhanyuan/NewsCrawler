#! /usr/bin/python3
# coding=utf-8

import datetime
import sys
sys.path.append("..")
from news_search.mongo_config import collection


def remove_article():
	collection.remove()


def add_article(url, article):
	# print(url)
	article_dict = {
		"url": url,
		"article": article,
		"time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	}
	if article is not None:
		try:
			collection.update_one(
				{"url": url},
				{'$setOnInsert': article_dict},
				upsert=True
			)
		except Exception as error:
			print(error)


def url_exist(url):
	results = collection.find({"url": url})
	for res in results:
		if res:
			return True
	return False


# if __name__ == '__main__':
# 	f = "hello world"
# 	add_article(f, f)
	# remove_article()
	# a = url_exist("http://news.ifeng.com/c/7j5UK9liHDc")
	# print(a)
