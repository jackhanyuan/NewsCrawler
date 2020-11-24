#! /usr/bin/python3
# coding=utf-8

import re
import jieba
from mongo_config import collection
import base64


# 检查是否有中文字符
def check_contain_chinese(check_str):
	for ch in check_str:
		if u'\u4e00' <= ch <= u'\u9fff':
			return True
	return False


# 搜索
def mongo_search(query):
	res = []

	# 如果有中文，优先中文完全匹配
	if check_contain_chinese(query):
		regx1 = re.compile(query, re.IGNORECASE)
		query1 = {"$and": [{"article.title": regx1}, {"article.content": regx1}]}
		results1 = collection.find(query1, {"_id": 1})
		for result in results1:
			if result not in res:
				# print(result["article"]['title'])
				# print(result)
				res.append(result)

	# 如果有中文，中文分词匹配
	if check_contain_chinese(query):

		# 分词
		query_list = jieba.cut_for_search(query)
		query_list = list(filter(lambda s: s and (type(s) != str or len(s.strip()) > 0), set(query_list)))
		# print(query_list)

		# 循环搜索
		for query_term in query_list:
			regx2 = re.compile(".*?" + query_term + ".*?", re.IGNORECASE)
			query2 = {"$and": [{"article.title": regx2}, {"article.content": regx2}]}
			results2 = collection.find(query2, {"_id": 1})
			# explain = results2.explai()  # 测试result2命令是否用索引
			# print(explain["executionStats"]['totalKeysExamined'])
			for result in results2:
				if result not in res:
					# print(result["article"]['title'])
					# print(result)
					res.append(result)

		for query_term in query_list:
			regx3 = re.compile(".*?" + query_term + ".*?", re.IGNORECASE)
			query3 = {"$or": [{"article.title": regx3}, {"article.content": regx3}]}
			results3 = collection.find(query3, {"_id": 1})
			for result in results3:
				if result not in res:
					# print(result["article"]['title'])
					# print(result)
					res.append(result)
	# print("-" * 50)

	# 如果全英文，英文文本完全匹配
	results3 = collection.find({"$text": {"$search": '"' + query + '"'}}, {"_id": 1, "score": {"$meta": 'textScore'}})
	results3 = sorted(results3, key=lambda k: -k['score'])
	# print(results3)

	for result in results3:
		# print(result['score'])
		del result['score']
		if result not in res:
			# print(result["article"]['title'])
			# print(result)
			res.append(result)

	# 如果全英文，英文文本部分匹配
	# results4 = collection.find({"$text": {"$search": query}}, {"score": {"$meta": 'textScore'}}).sort(
	# 	[('score', {'$meta': 'textScore'})]) # 此方法数据过大时会内存溢出
	# 不返回"article.images"数据，解决内存不足问题
	results4 = collection.find({"$text": {"$search": query}}, {"_id": 1, "score": {"$meta": 'textScore'}})
	results4 = sorted(results4, key=lambda k: -k['score'])
	# explain = results4.explain()  # 测试result2命令是否用索引
	# print(explain["executionStats"]['totalKeysExamined'])
	for result in results4:
		# print(result['score'])
		del result['score']
		if result not in res:
			# print(result["article"]['title'])
			res.append(result)
	# print(res)
	# print(len(res))
	# 改用只返回_id的方式以解决内存爆炸的问题
	return res


def content_search(id_list):
	res = []
	for id_dict in id_list:
		query_id = id_dict["_id"]
		result = collection.find({"_id": query_id}, {"article.images": 0})
		# explain = result.explain()  # 测试result2命令是否用索引
		# print(explain["executionStats"]['totalKeysExamined'])
		# print(result[0])
		res.append(result[0])
	return res


def snapshot_search(url):
	results = collection.find({"url": url})
	# explain = results.explain()  # 测试result2命令是否用索引
	# print(explain["executionStats"]['totalKeysExamined'])
	for res in results:
		return res


def str2img(url):
	res = snapshot_search(url)
	img_list = res["article"]["images"]
	images = []
	count = 0
	if img_list is not None:
		for img_data in img_list:
			count += 1
			n = url.rindex('/')
			file_name = re.sub(r'\W', '', url[n+1:])
			img_name = "snapshots/" + file_name + "_" + str(count) + ".jpg"
			with open("static/" + img_name, 'wb') as f:
				img = base64.b64decode(img_data)
				f.write(img)
			images.append(img_name)
	return images


# mongo_search('特朗普 November 20, 2020')
# r = snapshot_search("http://news.ifeng.com/c/7uxehhNwFJg")
# print(r)
# print(len(r["article"]["images"]))
# r2 = content_search(mongo_search('特朗普'))
# print(len(r2), r2)
# str2img("https://news.china.com/socialgd/10000169/20200610/38331646.html")
