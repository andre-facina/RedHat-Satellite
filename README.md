# RedHat-Satellite

This script establishes a connection with Red Hat Satellite, extracts host information, and generates a CSV file named hosts.csv. The script has been tested successfully on Red Hat Satellite version 6.12.

The following host information is extracted:

    Host Name
    Operating System
    Version
    IP Address
    Domain Name
    Organization
    Location
    Host Group Name
    Content View
    Life Cycle Environment
    Registration Date

To utilize this script, it's necessary to create an authentication token. You can achieve this by following these steps:

    Access Satellite's interface.
    Navigate to "Administer."
    Select the desired user.
    Choose "Personal Access Tokens."

Script Usage Syntax:
python3 redhat_satellite_hosts_info.py --url https://host.example.redhat.com --username user
