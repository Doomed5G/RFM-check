#!/usr/bin/env python3
"""RFM_CHECK"""
import csv
import os
from falconpy import Hosts
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def collect_api_data():
    '''Retrieve hostname, CID, OS version,.. etc from body'''
    #variable
    hosts = Hosts(client_id=client_id, client_secret=client_secret ,base_url= base_url)

    #Variable
    rfm_hosts = []

    # query to falcon host list
    result = hosts.query_devices_by_filter(limit=5000, sort="hostname|asc")

    #Filter device details from query results.
    if result["body"]["resources"]:
        detail = hosts.get_device_details(
        result["body"]["resources"]
        )["body"]["resources"]

    #export useful information
        for host in detail:
            if host.get('reduced_functionality_mode', 'yes') == "yes":

            # append to to work with list instead of dict.
                rfm_hosts.append( {
            "hostname": host.get("hostname", "unknown"),
            "reduced_functionality_mode": host.get("reduced_functionality_mode"),
            "os_version": host.get("os_version"),
            "platform_name": host.get("platform_name"),
            "agent_version": host.get("agent_version")
            })
    return rfm_hosts

#write list with data from api call to .csv file
def to_csv(name, api_body):
    '''create file and make it writable, newline after'''
    with open(name,'w', newline='', encoding="utf-8") as file:

        # Create fieldnames for DictWriter
        fieldnames = ['hostname', 'reduced_functionality_mode', 'os_version',
                     'platform_name', 'agent_version']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(api_body)

def data_to_sheets(name):
    """updating spreadsheet"""
    with open(name, mode='r', encoding="utf-8") as file:
        rfm_hosts_csv = file.read()
        client.import_csv(spreadsheet_id, rfm_hosts_csv)
    os.remove(name)


# main script
if __name__ == "__main__":
    #specific spreadsheet ID
    spreadsheet_id = os.environ['SHEET_ID']
    FILENAME = 'rfm_check.csv'
    # Load secrets
    client_id = os.environ['API_ID']
    client_secret = os.environ['API_SECRET']
    base_url = os.environ['API_URL']

    #gspread auth
    credentials = ServiceAccountCredentials.from_json_keyfile_name("account.json")
    client = gspread.authorize(credentials)
    data = collect_api_data()
    to_csv(FILENAME, data)
    data_to_sheets(FILENAME)
