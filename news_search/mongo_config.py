#! /usr/bin/python3
# coding=utf-8
import pymongo
import os
import shutil

client = pymongo.MongoClient(host='localhost', port=27017, connect=False)
# client = pymongo.MongoClient(host='119.45.239.159', port=27017, connect=False)
client.admin.authenticate("root", "4621", mechanism='SCRAM-SHA-1')
db = client.news
collection = db.articles

# # 建立索引
# # mongo shell 命令
# mongo -uroot -p4621
# use news

# db.articles.getIndexes()
#
# db.articles.dropIndex()
#
# db.articles.createIndex(
# 	{"article.title": 'text',
# 	  "article.content": 'text',
# 	  "article.publish_time": 'text',
# 	  "article.author": 'text',
# 	  "url": 'text',
# 	  "time": 'text'},
#
# 	{"weights":
# 		 {"article.title": 10,
# 		  "article.content": 5,
# 		  "article.publish_time": 12,
# 		  "article.author": 10,
# 		  "url": 8,
# 		  "time": 5},
#
# 	 "name": 'news_all_text_index',
# 	 "default_language": 'english',
#    "background": "True"
# 	 });

#
# db.articles.createIndex(
# 	{"article.title": 1,
# 	 "article.content": 1},
# 	{"name": "title_content_index",
# 	 "background": "True"});
#
# db.articles.createIndex(
# 	{"url": 1},
# 	{"name": "url_unique_index",
# 	 "background": "True",
# 	 "unique": "True"});


# # python内建立复合索引
# collection.create_index([("article.content", pymongo.DESCENDING),
#                          ("article.title", pymongo.DESCENDING)],
#                         background=True,
#                         name="title_content_index")
# # python内建立url唯一索引
# collection.create_index([("url", pymongo.DESCENDING)],
#                         background=True,
#                         unique=True,
#                         name="url_unique_index")
#
# # 建立全字段文本索引
# collection.create_index([("$**", pymongo.TEXT)],
#                         background=True,
#                         name="all_index")


# 删除索引
# collection.drop_index("title_content_index")
# collection.drop_index("all_index")
# collection.drop_index([("$**", pymongo.TEXT)])


# 删除快照目录图片缓存
def del_file(filepath):
	"""
	删除某一目录下的所有文件或文件夹
	:param filepath: 路径
	:return:
	"""
	del_list = os.listdir(filepath)
	for f in del_list:
		file_path = os.path.join(filepath, f)
		if os.path.isfile(file_path):
			os.remove(file_path)
		elif os.path.isdir(file_path):
			shutil.rmtree(file_path)


# del_file("./static/snapshots")