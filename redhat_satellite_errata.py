#This script extracts all RHSA, RHBA, and RHEA errata from Red Hat Satellite and saves them to a file named "errata.csv." It has been tested on Satellite 6.12. To use it, run the following command:
#python3 redhat_satellite_errata.py  --url https://host.example.redhat.com --username your_username --type [RHSA,RHBA,RHEA,ALL]

#   - Use RHSA to extract only RHSA (security) errata.
#   - Use RHBA to extract only RHBA (bugfix) errata.
#   - Use RHEA to extract only RHEA (enhancement) errata.
#   - Use ALL to extract all types of errata (RHSA, RHBA, RHEA).

# For the token it must be created in Administer -> Users -> An user  -> Personal Access Tokens

# Author: Andre Facina


import requests
import csv
import urllib3
import argparse
from getpass import getpass

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_errata_data(username, token, url, errata_id):
    errata_url = f"{url}/katello/api/errata/{errata_id}"
    try:
        response = requests.get(errata_url, auth=(username, token), verify=False)
        if response.status_code == 200:
            errata_data = response.json()
            return errata_data
        else:
            #print(f"Failed to fetch errata data. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def process_errata_data(errata_data):
    if not errata_data:
        return None

    errata_id = errata_data.get("errata_id", "")
    issued = errata_data.get("issued", "")
    severity = errata_data.get("severity", "")
    errata_type = errata_data.get("type", "")
    cves = ", ".join(cve["cve_id"] for cve in errata_data.get("cves", []))
    bugs = ", ".join(bug["bug_id"] for bug in errata_data.get("bugs", []))
    hosts_applicable_count = errata_data.get("hosts_applicable_count", "")
    packages = ", ".join(errata_data.get("packages", []))

    return [errata_id, issued, severity, errata_type, cves, bugs, hosts_applicable_count, packages]

def write_to_csv(data, filename):
    with open(filename, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["errata_id", "issued", "severity", "type", "cves", "bugs", "hosts_applicable_count", "packages"])
        csv_writer.writerows(data)
    print(f"Data has been written to {filename}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrieve and process errata data from a Red Hat Satellite API')
    parser.add_argument('--username', required=True, help='Username for authentication')
    parser.add_argument('--url', required=True, help='Base URL of Red Hat Satellite')
    parser.add_argument('--type', required=True, choices=['ALL', 'RHBA', 'RHSA', 'RHEA'], help='Type of errata to process')
    args = parser.parse_args()

    token = getpass("Token: ")

    errata_id = 1
    errata_data_list = []

    print(f'Retrieving errata information from {args.url}. This process may take several minutes...')

    while True:
        errata_data = fetch_errata_data(args.username, token, args.url, errata_id)
        if errata_data is None:
            break

        processed_data = process_errata_data(errata_data)

        if processed_data:
            errata_type = processed_data[3]

            if args.type == 'ALL' or (args.type == 'RHBA' and errata_type == 'bugfix') or \
                    (args.type == 'RHSA' and errata_type == 'security') or \
                    (args.type == 'RHEA' and errata_type == 'enhancement'):
                errata_data_list.append(processed_data)

        errata_id += 1

    write_to_csv(errata_data_list, "errata.csv")

