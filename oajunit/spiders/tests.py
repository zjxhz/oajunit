import scrapy
import re


class TestsSpider(scrapy.Spider):
    name = "tests"
    start_urls = [
        'http://atgebs.us.oracle.com/pub/DailyBuild/oafjunitreport/archive/',
    ]

    def parse(self, response):
        days = getattr(self, 'days', None)
        if days is None:
            days = 7
        for report in response.css('table a').re(r'>(jdev.*)<')[-int(days):]:
        	if report is not None:
        	    report = response.urljoin(report + "html/all-tests.html")
        	    yield scrapy.Request(report, callback=self.parse_report)

    def parse_report(self, response):
        name = re.search(r'/(jdev.*)/html', response.url).group(1)
        tests = []
        for row in response.css('.details tr')[1:]:
            class_name = row.xpath('td[1]/a/text()').extract_first()
            method_name = row.xpath('td[2]/a/text()').extract_first()
            status = row.xpath('td[3]/text()').extract_first()
            message = row.xpath('td[4]/text()').extract_first()
            time = row.xpath('td[5]/text()').extract_first()
            tests.append({
                'name': class_name + '#' + method_name,
                'status': status,
                'message': message,
                'time': time,
            })
        yield {'name': name, 'tests': tests}
