import json
import xml.etree.ElementTree as ET
import re
import xml.dom.minidom

def get_alway_failures(all_failures):
    always_failures = all_failures[0]
    for failures in all_failures:
        always_failures = always_failures & failures
    return always_failures

def replace_template(template, token, result):
    return template.replace('{{%s}}'  % token, str(result))

def create_table():
    table = ET.Element('table')
    table.set('class', 'table table-striped test-report-table')
    return table

def get_failures_today(all_failures):
    failures_today = all_failures[-1]
    failures_yesterday = all_failures[-2]
    return failures_today - failures_yesterday

def get_passed_today(all_failures):
    failures_today = all_failures[-1]
    failures_yesterday = all_failures[-2]
    return failures_yesterday - failures_today

def replace_overview(data, all_failures, merged_failures):
    always_failures = get_alway_failures(all_failures)
    failed_today_count = len(get_failures_today(all_failures) )
    passed_today_count = len(get_passed_today(all_failures) )
    always_failures_count = len(always_failures)
    occationally_failed_count = len(merged_failures - always_failures)

    table = ET.Element('table')
    table.set('class', 'table table-striped test-report-table')
    header = ET.SubElement(table, 'thead')
    row = ET.SubElement(header, 'tr')
    test_name_header = ET.SubElement(row, 'th')
    test_name_header.set('class','test-name-header')
    test_name_header.text = 'Test'
    for sorted_report in sorted(data, key=lambda report: report['name']):
        date = re.search(r'_(\d{2}_\d{2})', sorted_report['name']).group(1)
        date_header = ET.SubElement(row, 'th')
        date_header.text = date
    tbody = ET.SubElement(table, 'tbody')
    for failure in merged_failures:
        row = ET.SubElement(tbody, 'tr')
        test_name_cell = ET.SubElement(row, 'td')
        #class_name = failure[:failure.index('#')]
        #method_name = failure[failure.index('#') + 1:]
        test_name_cell.text = failure
        test_name_cell.set('class', 'test-name-col ')
        for daily_failures in all_failures:
            cell = ET.SubElement(row, 'td')
            icon = ET.SubElement(cell, 'span')
            icon.set('class', 'test-status-icon glyphicon')
            if failure in  daily_failures:
                icon.set('class', icon.get('class') + ' glyphicon-remove text-danger')
            else:
                icon.set('class', icon.get('class') + ' glyphicon-ok text-success')

    template = open('html/oajunit_template.html', 'r').read()
    xml = ET.tostring(table)
    #pretty_xml = xml.dom.minidom.parse().toprettyxml(xml)
    output = replace_template(template, 'table', xml)
    output = replace_template(output, 'failed_today', failed_today_count)
    output = replace_template(output, 'passed_today', passed_today_count)
    output = replace_template(output, 'always_failed', always_failures_count)
    output = replace_template(output, 'occationally_failed', occationally_failed_count)
    output_html = open('html/oajunit.html', 'w')
    output_html.write(output)
    output_html.close()

def replace_detail(failures, description, filename):
    table = ET.Element('table')
    table.set('class', 'table table-striped')
    header = ET.SubElement(table, 'thead')
    row = ET.SubElement(header, 'tr')
    test_num_header  = ET.SubElement(row, 'th')
    test_num_header.text = '#'
    test_name_header = ET.SubElement(row, 'th')
    test_name_header.text = 'Test'
    test_num = 1
    tbody = ET.SubElement(table, 'tbody')
    for failure in failures:
        row = ET.SubElement(tbody, 'tr')
        test_num_cell = ET.SubElement(row, 'td')
        test_num_cell.text = str(test_num)
        test_num += 1
        test_name_cell = ET.SubElement(row, 'td')
        test_name_cell.text = failure

    template = open('html/detail_template.html', 'r').read()
    xml = ET.tostring(table)
    output = replace_template(template, 'table', xml)
    output = replace_template(output, 'description', description)
    output_html = open('html/oajunit-%s.html' % filename, 'w')
    output_html.write(output)
    output_html.close()

def main():
    content = open('tests.json','r').read()
    data = json.loads(content)

    all_failures = []
    merged_failures = set()

    for sorted_report in sorted(data, key=lambda report: report['name']):
        failures = set()
        for test in  sorted_report['tests']:
            if not test['status'] == 'Success':
                failures.add(test['name'])
                merged_failures.add(test['name'])
        all_failures.append(failures)

    replace_overview(data, all_failures, merged_failures)
    replace_detail(get_failures_today(all_failures), "Today+", "added-today")
    replace_detail(get_passed_today(all_failures), "Today-", "passed-today")
    always_failures = get_alway_failures(all_failures)
    occationally_failed= merged_failures - always_failures
    replace_detail(always_failures, "Always", "always-failed")
    replace_detail(occationally_failed, "Occational", "occationally-failed")



if __name__ == '__main__':    
    main()


