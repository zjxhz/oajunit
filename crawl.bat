@echo off
del tests.json
scrapy crawl tests -o tests.json -a days=7