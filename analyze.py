import json
import xml.etree.ElementTree as ET
import re
import xml.dom.minidom


def get_always_failures(all_failures):
    always_failures = all_failures[0]
    for failures in all_failures:
        always_failures = always_failures & failures
    return always_failures


def replace_template(template, token, result):
    return template.replace('{{%s}}' % token, str(result))


def get_failures_today(all_failures):
    failures_today = all_failures[-1]
    failures_yesterday = all_failures[-2]
    return failures_today - failures_yesterday


def get_passed_today(all_failures):
    failures_today = all_failures[-1]
    failures_yesterday = all_failures[-2]
    return failures_yesterday - failures_today


def replace_trend(template, data, all_failures, merged_failures):
    always_failures = get_always_failures(all_failures)
    failed_today_count = len(get_failures_today(all_failures))
    passed_today_count = len(get_passed_today(all_failures))
    always_failures_count = len(always_failures)
    occationally_failed_count = len(merged_failures - always_failures)

    table = ET.Element('table')
    table.set('id', 'table_trend')
    table.set('class', 'table table-striped table-tests test-trend-table')
    header = ET.SubElement(table, 'thead')
    row = ET.SubElement(header, 'tr')
    test_name_header = ET.SubElement(row, 'th')
    test_name_header.set('class', 'test-name-header')
    test_name_header.text = 'Test'
    for sorted_report in sorted(data, key=lambda report: report['name']):
        date = re.search(r'_(\d{2}_\d{2})', sorted_report['name']).group(1)
        date_header = ET.SubElement(row, 'th')
        date_header.text = date
    tbody = ET.SubElement(table, 'tbody')
    for failure in merged_failures:
        row = ET.SubElement(tbody, 'tr')
        test_name_cell = ET.SubElement(row, 'td')
        # class_name = failure[:failure.index('#')]
        # method_name = failure[failure.index('#') + 1:]
        test_name_cell.text = failure
        test_name_cell.set('class', 'test-name-col ')
        for daily_failures in all_failures:
            cell = ET.SubElement(row, 'td')
            icon = ET.SubElement(cell, 'span')
            icon.set('class', 'test-status-icon glyphicon')
            if failure in daily_failures:
                icon.set('class', icon.get('class') + ' glyphicon-remove text-danger')
            else:
                icon.set('class', icon.get('class') + ' glyphicon-ok text-success')

    xml = ET.tostring(table)
    # pretty_xml = xml.dom.minidom.parse().toprettyxml(xml)
    output = replace_template(template, 'table_trend', xml)
    output = replace_template(output, 'failed_today', failed_today_count)
    output = replace_template(output, 'merged_failure_count', len(merged_failures))
    output = replace_template(output, 'always_failed', always_failures_count)
    output = replace_template(output, 'occationally_failed', occationally_failed_count)
    return output


def replace_detail(output, failures, description, table_name):
    table = ET.Element('table')
    table.set('id', table_name)
    table.set('class', 'table table-striped table-tests')
    # table.set('style', 'display:none')
    header = ET.SubElement(table, 'thead')
    row = ET.SubElement(header, 'tr')
    test_num_header = ET.SubElement(row, 'th')
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

    xml = ET.tostring(table)
    return replace_template(output, table_name, xml)


def main():
    content = open('tests_weekly.json', 'r').read()
    data = json.loads(content)

    all_failures = []
    merged_failures = set()

    for sorted_report in sorted(data, key=lambda report: report['name']):
        failures = set()
        for test in sorted_report['tests']:
            if not test['status'] == 'Success':
                failures.add(test['name'])
                merged_failures.add(test['name'])
        all_failures.append(failures)

    always_failures = get_always_failures(all_failures)
    occationally_failed = merged_failures - always_failures

    template = open('html/oajunit_template.html', 'r').read()
    output = replace_trend(template, data, all_failures, merged_failures)
    output = replace_detail(output, get_failures_today(all_failures), "Today+", "table_today")
    output = replace_detail(output, always_failures, "Always", "table_always")
    output = replace_detail(output, occationally_failed, "Occational", "table_occational")
    output_html = open('html/oajunit.html', 'w')
    output_html.write(output)
    output_html.close()


if __name__ == '__main__':
    main()
