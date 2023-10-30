import csv
import json
import argparse
from datetime import datetime

#Constantes adicionadas
SCHEMA_FILE = 'itil.change.schema.json'
DATETIME_FORMAT = '%m/%d/%Y %H:%M'
RFC3339_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

def to_rfc3339(dt_str):
    """Convert a datetime string to RFC3339 format."""
    dt_obj = datetime.strptime(dt_str, DATETIME_FORMAT)
    return dt_obj.strftime(RFC3339_FORMAT)

def read_schema():
    """Read and return the JSON schema from file."""
    with open(SCHEMA_FILE, 'r') as file:
        return json.load(file)

def read_csv_data(csv_file):
    """Read the CSV data and return a list of ticket dicts."""
    with open(csv_file, 'r', newline='', encoding='utf-8-sig') as file: 
        reader = csv.DictReader(file)
        return [{
            "ticket_id": row['change_id'],
            "tool_type": "Remedy",
            "short_description": row['summary'],
            "long_description": row['description'],
            "approval": row['approval_status'],
            "status": row['Success_Code'],
            "assignment_group": row['requester_group'],
            "category": row['category'],
            "change_type": row['type'],
            "backout_plan": row['backout_plans'],
            "justification": row['reason_aots'],
            "exception_reason": row['exception_justification'],
            "configuration_item": row['category_cd'],
            "location_street": row['person_address1'],
            "location_city": row['region'],
            "location": row['person_city'],
            "location_country": row['person_country'],
            "impact": row['impact'],
            "urgency": row['priority'],
            "priority": row['employee_priority'],
            "risk-impact-analysis": row['business_risk_aots'],
            "completion_code": row['Success_Code'],
            "modified_datetime": to_rfc3339(row['modified_date']),
            "opened_datetime": to_rfc3339(row['date_created_central']),
            
        } for row in reader]

def write_output(schema, output_file):
    """Write the updated schema to the output file."""
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(schema, file, ensure_ascii=False, indent=4)

def process_data(csv_file):
    """Process the data and write to JSON."""
    schema = read_schema()
    tickets = read_csv_data(csv_file)
    schema['items'] = tickets
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    output_file = f'itil.change.{now}.json'
    write_output(schema, output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process a CSV file and output to JSON.')
    parser.add_argument('csv_file', help='The path to the CSV file to process.')
    args = parser.parse_args()
    process_data(args.csv_file)
