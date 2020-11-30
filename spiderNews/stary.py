'''
    Copyright (C) 2020 All rights reserved.

    FileName      ：stary.py
    Author        ：LYC
    Email         ：991688344@qq.com
    Date          ：2020年11月30日
    Description   ：
'''
from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#print(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy.exe', 'crawl', 'spiderBilibiliNews','-s','LOG_FILE=scrapy.log'])

