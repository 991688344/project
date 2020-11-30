# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import codecs
import json
import os
import wordcloud
import numpy
import PIL.Image as Image
import time
#from scrapy.exporters import JsonItemExporter,JsonLinesItemExporter

class SpidernewsPipeline:
    def __init__(self):
        #self.fp=open("BilibiliRank.json",'wb')
        #self.exporter = JsonLinesItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')
        self.json_file = codecs.open('news.json','w+',encoding='UTF-8')

    def open_spider(self,spider):
        print("[*] 爬虫开始了...")
        # 在爬虫开始时，首先写入一个 '[' 符号，构造一个 json 数组']'
        self.json_file.write('[\n')

    def process_item(self, item, spider):
        #self.exporter.export_item(item)
        item_json = json.dumps(dict(item), ensure_ascii=False)
        self.json_file.write('\t' + item_json + ',\n')
        #print(f"[*] from pipline: {item_json}")
        return item

    def close_spider(self,spider):
        # 在结束后，需要对 process_item 最后一次执行输出的 “逗号” 去除
        # 当前文件指针处于文件尾，使用 SEEK 方法，定位文件尾前的两个字符（一个','(逗号), 一个'\n'(换行符)） 的位置
        self.json_file.seek(-2, os.SEEK_END)
        # 使用 truncate() 方法，将后面的数据清空
        self.json_file.truncate()
        # 重新输出'\n'，并输入']'，与 open_spider(self, spider) 时输出的 '['，构成一个完整的数组格式
        self.json_file.write('\n]')
        # 关闭文件
        self.json_file.close()
        print("[*] 爬虫结束了...")
        print("[*] 文件保存在 news.json , images/Rank.png")
        self.plotWordCloud()

    def plotWordCloud(self):
        '''
        绘制词云图
        '''
        content = ""
        with open(r"news.json","rb") as f:
            data = json.load(f)
        for i in data:
            content = content +  " ".join([t for t in i['tag']])
            content = content + " "
        content = content.replace("资讯 ","")     # 去除资讯,环球标签
        content = content.replace("环球 ","")
        content = content.replace("星海计划 ","")
        content = content.replace("星海计划","")
        print(f"[*] 所有tag{content}")
        # 生成词云
        mask_pic=numpy.array(Image.open("images/cloud.jpg"))    # 图片遮罩层
        wc = wordcloud.WordCloud(
            font_path='font/FZSTK.TTF',  # 字体路径
            background_color='black',  # 背景颜色
            width=1000,
            height=800,
            max_font_size=50,  # 字体大小
            min_font_size=10,
            mask=mask_pic,  # 背景图片
            max_words=1000
        )
        wc.generate(content)
        wc.to_file('images/Rank.png')  # 图片保存
        image = wc.to_image()
        image.show()
