# RFM-check
Python script that collects hosts in RFM on CrowdStrike Falcon using the API and FalconPy SDK .\
Gathers Hostname, OS, OS version, and current version of the Falcon agent installed on the hosts that are currently in RFM.
The script will convert the gathered metadata to CSV and upload it to google sheets using gspread SDK and google API. 


