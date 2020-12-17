#! /usr/bin/python3
# coding=utf-8
import pymongo


# client = pymongo.MongoClient(host='localhost', port=27017, connect=False)
client = pymongo.MongoClient(host='119.45.239.159', port=27017, connect=False)
client.admin.authenticate("root", "4621", mechanism='SCRAM-SHA-1')
db = client.news
articles_collection = db.articles
snapshots_collection = db.snapshots

# # 建立索引
# # mongo shell 命令
# mongo -uroot -p4621
# use news

# db.articles.getIndexes()
# db.articles.dropIndex()
#
# db.snapshots.getIndexes()
# db.snapshots.dropIndex()
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
# 	 "name": 'articles_all_text_index',
# 	 "default_language": 'english',
#    "background": "True"
# 	 });
#
#
# db.articles.createIndex(
# 	{"article.title": 1,
# 	 "article.content": 1},
# 	{"name": "articles_title_content_index",
# 	 "background": "True"});
#
# db.articles.createIndex(
# 	{"url": 1},
# 	{"name": "articles_url_unique_index",
# 	 "background": "True",
# 	 "unique": "True"});
#
# db.snapshots.createIndex(
# 	{"url": 1},
# 	{"name": "snapshots_url_unique_index",
# 	 "background": "True",
# 	 "unique": "True"});


# # python内建立复合索引
# articles_collection.create_index([("article.content", pymongo.DESCENDING),
#                          ("article.title", pymongo.DESCENDING)],
#                         background=True,
#                         name="articles_title_content_index")
# # python内建立url唯一索引
# articles_collection.create_index([("url", pymongo.DESCENDING)],
#                         background=True,
#                         unique=True,
#                         name="articles_url_unique_index")
#
# snapshots_collection.create_index([("url", pymongo.DESCENDING)],
#                         background=True,
#                         unique=True,
#                         name="snapshots_url_unique_index")
#
# # 建立全字段文本索引
# articles_collection.create_index([("$**", pymongo.TEXT)],
#                         background=True,
#                         name="articles_all_text_index")


# 删除索引
# articles_collection.drop_index("articles_title_content_index")
# articles_collection.drop_index("articles_url_unique_index")
# snapshots_collection.drop_index("snapshots_url_unique_index")
# articles_collection.drop_index([("$**", pymongo.TEXT)])


