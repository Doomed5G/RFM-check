# RFM-check
Python script that interacts with CrowdStrike Falcon API and collects all hosts with sensors in RFM.\
Gathers Hostname, OS, OS version, and current version of the Falcon agent installed on the hosts that are currently in RFM.\
The script will convert the gathered metadata to CSV and upload it to google sheets using gspread SDK and google API. 


