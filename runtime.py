import json
import re


def main():
    content = open('tests_weekly.json', 'r').read()
    data = json.loads(content)
    time_dict = {}
    for sorted_report in sorted(data, key=lambda report: report['name']):
        date = re.search(r'_(\d{2}_\d{2})', sorted_report['name']).group(1)
        for test in sorted_report['tests']:
            test_name = test['name']
            if test_name not in time_dict:
                time_dict[test_name] = {'time': {}}

            t = time_dict[test['name']]
            if 'first_time' not in t:
                t['first_time'] = float(test['time'])
            t['time'][date] = float(test['time'])
            t['diff'] = t['time'][date] - t['first_time']
    for t in sorted(time_dict, key=lambda temp: time_dict[temp]['diff']):
        print t['diff']
    with open('tests_weekly_ex.json', 'w') as f:
        json.dump(time_dict, f, indent=2)


if __name__ == '__main__':
    main()
