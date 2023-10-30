import csv
import json
import argparse
from datetime import datetime

SCHEMA_FILE = 'itil.incident.schema.json'
DATETIME_FORMAT = '%m/%d/%Y %H:%M'
RFC3339_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

def to_rfc3339(dt_str):
    """Convert a datetime string to RFC3339 format."""
    if not dt_str:  # Verify if the string is empty to not break the code in case of tickets that are not closed.
        return None
    dt_obj = datetime.strptime(dt_str, DATETIME_FORMAT)
    return dt_obj.strftime(RFC3339_FORMAT)

def read_schema():
    """Read and return the JSON schema from file."""
    with open(SCHEMA_FILE, 'r') as file:
        return json.load(file)

def read_csv_data(csv_file):
    """Read the CSV data and return a list of ticket dicts."""
    with open(csv_file, newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        return [{
            "ticket_id": row['ticket'],
            "short_description": row['problem_abstract'],
            "long_description": row['problem_abstract'],
            "tool_type": "Remedy",
            "cause": row['sub_root_cause_desc_tx'],
            "cause_code": row['root_cause_desc_tx'],
            "status": row['state'],
            "priority": row['severity'],
            "assignment_group": row['work_queue'],
            "configuration_item": row['reported_asset_id'],
            "resolution_code": row['resol_action_desc_tx'],
            "modified_datetime": to_rfc3339(row['last_modified_date']),
            "opened_datetime": to_rfc3339(row['ticket_opened']),
            "closed_datetime": to_rfc3339(row['ticket_closed']),
            "resolved_datetime": to_rfc3339(row['service_restored_date']),
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
    output_file = f'itil.incident.{now}.json'
    write_output(schema, output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process a CSV file and output to JSON.')
    parser.add_argument('csv_file', help='The path to the CSV file to process.')
    args = parser.parse_args()
    process_data(args.csv_file)