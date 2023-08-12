# This script interfaces with the Red Hat Satellite API to retrieve information about content views. Subsequently, it compiles this data and exports it to an Excel spreadsheet. Each sheet within the workbook corresponds to a specific content view, showcasing details such as content view version, latest update, activation key status, and repository listings. The name of the Excel file created will be content_views_[Organization].xlsx. For the tokens it must be created in Administer -> Users -> An user  -> Personal Access Tokens
# Author: Andre Facina

import requests
import json
import csv
import re
import urllib3
import argparse
from getpass import getpass
from openpyxl import Workbook

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to extract content view information
def extract_content_view_info(content_view):
    version = content_view["latest_version"]
    lifecycle_names = [env["name"] for env in content_view["latest_version_environments"]]
    
    last_task = content_view.get("last_task")
    last_sync = last_task.get("started_at") if last_task else "N/A"
    
    repositories = [repo["name"] for repo in content_view["repositories"]]
    activation_keys = [key["name"] for key in content_view["activation_keys"]]
    
    return version, lifecycle_names, last_sync, repositories, activation_keys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrieve Content View information from Red Hat Satellite API')
    parser.add_argument('--username', required=True, help='Username for authentication')
    parser.add_argument('--url', required=True, help='Base URL Red Hat Satellite')
    parser.add_argument('--organization', required=True, help='Organization name')
    args = parser.parse_args()

    token = getpass("Token: ")
    headers = {'Accept': 'application/json'}

    # Find organization ID from the organization name
    org_url = args.url + '/katello/api/organizations'
    response = requests.get(org_url, auth=(args.username, token), headers=headers, verify=False)
    
    org_id = None
    if response.status_code == 200:
        org_data = response.json()
        for org in org_data["results"]:
            if org["name"] == args.organization:
                org_id = org["id"]
                break

    if org_id is None:
        print(f"Organization '{args.organization}' not found.")
        exit(1)
    
    url_content_views = args.url + f'/katello/api/organizations/{org_id}/content_views'
    response = requests.get(url_content_views, auth=(args.username, token), headers=headers, verify=False)
    
    if response.status_code == 200:
        content_views_data = response.json()
        content_views = content_views_data["results"]
        
        # Excel
        workbook = Workbook()
        
        for content_view in content_views:
            cv_name = content_view["name"]
            version, lifecycle_names, last_sync, repositories, activation_keys = extract_content_view_info(content_view)
            
            sheet = workbook.create_sheet(cv_name)
            #sheet.append(["Attribute", "Value"])
            sheet.append(["Content View Version", version])
            sheet.append(["Last Sync", last_sync])
            # Write activation keys in separate columns if present
            sheet.append(["##### Activation Key #####"])
            sheet.append(["Activation Key " + str(i+1) for i in range(len(activation_keys))])
            sheet.append(activation_keys)
            # Write lifecycles (Environments) in separate columns
            sheet.append(["##### Environments #####"])
            sheet.append(["Environment " + str(i+1) for i in range(len(lifecycle_names))])
            sheet.append(lifecycle_names)

            sheet.append(["##### Repositories #####"])
            # Write repositories in separate columns
            sheet.append(["Repository " + str(i+1) for i in range(len(repositories))])
            sheet.append(repositories)
            
        
        workbook.remove(workbook["Sheet"]) 
        # The name of the Excel file is content_views_[Organization].xlsx
        excel_file = f"content_views_{args.organization}.xlsx"
        workbook.save(excel_file)
        
        print(f"Data has been written to {excel_file}")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print("Response:")
        print(response.text)

