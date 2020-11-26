#! /usr/bin/python3
# coding=utf-8

import sys
sys.path.append("..")
from news_search.mongo_config import articles_collection, snapshots_collection


def remove_article():
	articles_collection.remove()


def add_article(url, article):
	# print(url)
	snapshots_dict = {
		"url": url,
		"article.content_html": article['content_html'],
		"article.images": article['images']
	}

	snapshots_collection.update_one(
		{"url": url},
		{'$setOnInsert': snapshots_dict},
		upsert=True
	)

	del article['content_html']
	del article['images']
	# print("\t" + article)

	article_dict = {
		"url": url,
		"article": article
	}

	articles_collection.update_one(
		{"url": url},
		{'$setOnInsert': article_dict},
		upsert=True
	)


def url_exist(url):
	results = articles_collection.find({"url": url})
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
