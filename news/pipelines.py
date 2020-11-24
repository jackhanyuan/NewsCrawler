#! /usr/bin/python3
# coding=utf-8

import pymysql
from twisted.enterprise import adbapi
import re
from datetime import datetime, timedelta
import pytz


def difTime(sqlTime):
    # monDict = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monDict = {
        'Jan': 1, 'Feb': 2, 'Mar': 3,
        'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9,
        'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    dateTup = re.match(r'.+?([0-9]{1,2})\s([A-Z][a-z]{2})\s([0-9]{4})\s([0-9]{2}:[0-9]{2}:[0-9]{2}).*', sqlTime).groups()
    dateStr = dateTup[2] + '-' + str(monDict[dateTup[1]]) + '-' + dateTup[0] + ' ' + dateTup[3]
    dateTime = datetime.strptime(dateStr,"%Y-%m-%d %H:%M:%S")
    dateTime = dateTime.replace(tzinfo=pytz.timezone('GMT'))
    # print(dateTime)
    nowTime = datetime.now(pytz.timezone('GMT'))
    # print((nowTime - dateTime).seconds)
    # print(nowTime)
    # print(dateTime)
    return (nowTime - dateTime).seconds


# 异步更新操作
class NewsPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
 

    @classmethod
    def from_settings(cls, settings):  # 函数名固定，会被scrapy调用，直接可用settings的值
        """
        数据库建立连接
        :param settings: 配置参数
        :return: 实例化参数
        """
        adbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            cursorclass=pymysql.cursors.DictCursor   # 指定cursor类型
        )
 
        # 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
        dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
        # 返回实例化参数
        return cls(dbpool)
 

    def process_item(self, item, spider):
        """
        使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
        """
        query = self.dbpool.runInteraction(self.do_insert, item)  # 指定操作方法和操作数据
        # 添加异常处理
        query.addCallback(self.handle_error)  # 处理异常
 

    def do_insert(self, cursor, item):
        # 对数据库进行插入操作，并不需要commit，twisted会自动commit
        insert_sql = "insert into urls (url, time, judge, isdelete) values (%s, %s, 'no', 'no');"
        inquire_sql = "select time from urls where url = %s;"
        update_sql = "update urls set time = %s, judge = 'no' where url = %s;"

        if not re.search(r'.*?(index|video?).*', item['url'], re.I):
            #if not re.search('index', item['url']):
            cursor.execute(inquire_sql, item['url'])
            n = cursor.fetchall()
            # print(n)
            if not n:
                try:
                    cursor.execute(insert_sql, (item['url'], item['time']))
                except:
                    pass
            elif difTime(n[0]['time']) > 7200:
                cursor.execute(update_sql, (item['time'], item['url']))
 

    def handle_error(self, failure):
        if failure:
            # 打印错误信息
            print(failure)
