#! /usr/bin/python3
# coding=utf-8


import pymysql
from outline_data import get_article
from save_data import add_article, url_exist
import datetime
import random

db = pymysql.connect(host='localhost', user='root', port=3306, passwd='4621', db='NEWS', use_unicode=True)


def sql_time():
	gmt_format = '%a, %d %b %Y %H:%M:%S GMT'
	s_time = datetime.datetime.utcnow().strftime(gmt_format)
	# print(sql_time)
	return s_time


def get_url():
	cursor = db.cursor()
	cursor.execute('select url from urls where judge = "no" and isdelete = "no";')
	urls = cursor.fetchall()
	url_list = list(urls)
	db.commit()
	cursor.close()
	random.shuffle(url_list)
	return url_list


def get_url_numbers():
	cursor = db.cursor()
	cursor.execute('select url from urls where judge = "no";')
	numbers = len(cursor.fetchall())
	db.commit()
	cursor.close()
	return numbers


def set_url(url):
	cursor1 = db.cursor()
	if url:
		n = cursor1.execute('update urls set judge = "yes", time = %s where url = %s;', (sql_time(), url))
		print("\tSet {} url effect".format(n))
	db.commit()
	cursor1.close()


def delete(url):
	cursor1 = db.cursor()
	if url:
		n = cursor1.execute('update urls set isdelete = "yes", time = %s where url = %s;', (sql_time(), url))
		print("\tDelete {} url effect".format(n))
	db.commit()
	cursor1.close()


def get_essay(url):
	if not url_exist(url[0]):
		print(url[0])
		article = get_article(url[0])
		if article is not None:
			if article != "Exception":
				add_article(url[0], article)
				set_url(url[0])
				print("\tTrue, get article successfully ")
		else:
			# set_url(url[0])
			delete(url[0])
			print("\tFalse, article is empty")
	else:
		print(url[0])
		set_url(url[0])
		print("\tFalse, article already exists")


# if __name__ == "__main__":
# 	u = ["https://dy.163.com/article/FSC51I8R0514C9B7.html", "http://news.ifeng.com/c/7kyf1it2RUx","http://www.xinhuanet.com/2019-08/26/c_1124923784.htm"]
# 	get_essay(u)
# n = get_url_numbers()
# get_url()
# 	delete("http://news.ifeng.com/c/7qVFnhzQf44")
