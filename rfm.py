#!/usr/bin/env python3
from falconpy import Hosts
import csv
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials


#specific speadsheet ID 
spreadsheet_id = os.environ['SHEET_ID']
filename = 'rfm_check.csv'
# Load secrets 
client_id = os.environ['API_ID']
client_secret = os.environ['API_SECRET']
base_url = os.environ['API_URL']

#gspread auth
creds = ServiceAccountCredentials.from_json_keyfile_name("account.json")
client = gspread.authorize(creds)

"""Retrieve hostname, CID, OS version,.. etc from body"""
def collect_api_data():
    # Make sure to not hardcode secrets!!!
    # API call authentication id, secret and base URL.  
    hosts = Hosts(client_id=client_id, client_secret=client_secret ,base_url= base_url)

    #Variable
    list = []

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
             list.append( {
            "hostname": host.get("hostname", "unknown"),
            "reduced_functionality_mode": host.get("reduced_functionality_mode"),
            "os_version": host.get("os_version"),
            "platform_name": host.get("platform_name"),
            "agent_version": host.get("agent_version")
            })
    return list

#write list with data from api call to .csv file
def to_csv(filename, data):
    #create file and make it writable, newline after ''
    with open(filename,'w', newline='') as file:

        # Create fieldnames for DictWriter
        fieldnames = ['hostname', 'reduced_functionality_mode', 'os_version', 'platform_name', 'agent_version']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
       
#updating spreadsheet
def data_to_sheets(filename):
    with open(filename, mode='r') as file:
        csv = file.read()
        client.import_csv(spreadsheet_id, csv)
    os.remove(filename)


# main script
if __name__ == "__main__":
    #specific speadsheet ID 
    spreadsheet_id = os.environ['SHEET_ID']
    filename = 'rfm_check.csv'
    # Load secrets 
    client_id = os.environ['API_ID']
    client_secret = os.environ['API_SECRET']
    base_url = os.environ['API_URL']

    #gspread auth
    creds = ServiceAccountCredentials.from_json_keyfile_name("account.json")
    client = gspread.authorize(creds)
    data = collect_api_data()
    to_csv(filename, data)
    data_to_sheets(filename)