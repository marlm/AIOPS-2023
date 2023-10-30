import csv
import json

csv_file = '/home/dassisbr/ATT_GIT/AIOPS/Remedy/csvchgout.csv'
json_file = 'change_out.json'

"""
required_fields = {
    "ticket",
    "short_description",
    "long_description",
    "status",
    "priority",
    "assignment_group",
    "opened_datetime",
    "modified_datetime"
}
"""

def csv_to_json(csv_file, json_file):
    data = []


    with open(csv_file, 'r', encoding='utf-8') as csvf:
        #csv_reader = csv.reader(csvf, delimiter=',')
        csv_reader = csv.DictReader(csvf, delimiter=',')

        for row in csv_reader:
            data.append(row)

    with open(json_file, 'w') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

if __name__ == '__main__':
    csv_to_json(csv_file, json_file)