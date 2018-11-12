# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2


class CloudRedisPipeline(object):
    def process_item(self, item, spider):
        conn = psycopg2.connect(database="mydb", user="yangmao", password="wangji522", host="118.24.89.181", port="5432")
        cur = conn.cursor()
        sql = "insert into music values(%s,%s) "
        cur.execute(sql, (item['music_name'], item['music_id']))
        conn.commit()
        cur.close()
        conn.close()
        return item
