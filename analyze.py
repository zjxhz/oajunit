import json

content = open('tests.json','r').read()
data = json.loads(content)

all_failures = []
for sorted_report in sorted(data, key=lambda report: report['name']):
    failures = set()
    for test in  sorted_report['tests']:
        if not test['status'] == 'Success':
            failures.add(test['name'])
    all_failures.append(failures)

failures1 = all_failures[-1]
failures2 = all_failures[-2]

print failures2 - failures1
print len(failures2 - failures1)
