# This script connects to Red Hat Satellite, extracts the hosts and create a file hosts.csv. Tested in Red Hat Satellite version 6.12
# The information extract are:
# Name,Operating System,Version,IP Address,Domain Name,Organization,Location,HostGroup Name,Content View,LifeCycle Environment,Registered Date
# To use it you must create a token. To do this go to Satellite -> Administer -> choose the user -> Personal Access Tokens
# The syntax to use the script is: python3 redhat_satellite_hosts_info.py --url https://host.example.redhat.com --username admin
# Then the script will ask to enter the token
# Author: Andre Facina

import requests
import json
import csv
import re
import urllib3
import argparse
from getpass import getpass

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def verify_api_status(username, token, url):
    url_status = url + '/api/status'
    #print(url_status)
    try:
        response = requests.get(url_status, auth=(username, token), verify=False)
        if response.status_code == 200:
            # Authentication successful
            print("Authentication successful!")
            print("API Status:")
            print(response.json())
        else:
            print(f"Failed to authenticate. Status code: {response.status_code}")
            print("Response:")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def get_hosts_information(username, token, url):
    url_hosts = url + '/api/v2/hosts'
    try:
        response = requests.get(url_hosts, auth=(username, token), verify=False)

        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])

            if not results:
                print("No hosts found in the response.")
                return

            #host_data = [(host["name"], host["operatingsystem_name"], host["ip"], host["domain_name"], host["organization_name"], host["location_name"], host["hostgroup_name"], host["subscription_facet_attributes"].get("id") ) for host in results]

            host_data = []
            for host in results:
                name = host["name"]
                os_name = host["operatingsystem_name"]
                ip = host["ip"]
                domain = host["domain_name"]
                org = host["organization_name"]
                location = host["location_name"]
                hostgroup = host["hostgroup_name"]

                content_view = host.get("content_facet_attributes", {}).get("content_view_name")
                lifecycle_env = host.get("content_facet_attributes", {}).get("lifecycle_environment_name")

                registered_at = host.get("subscription_facet_attributes", {}).get("registered_at")
                rh_version = host.get("subscription_facet_attributes", {}).get("release_version")

                host_data.append((name, os_name, rh_version, ip, domain, org, location, hostgroup, content_view, lifecycle_env, registered_at ))

            with open("hosts.csv", "w", newline="") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Name", "Operating System", "Version", "IP Address", "Domain Name", "Organization", "Location", "HostGroup Name", "Content View", "LifeCycle Environment", "Registered Date" ])
                csv_writer.writerows(host_data)

            print("Data has been written to hosts.csv")
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            print("Response:")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrieve host information from an Red Hat Satellite API')
    parser.add_argument('--username', required=True, help='Username for authentication')
    parser.add_argument('--url', required=True, help='Base URL Red Hat Satellite ')
    args = parser.parse_args()

    token = getpass("Token: ")

    verify_api_status(args.username, token, args.url)
    get_hosts_information(args.username, token, args.url)


