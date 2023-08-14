# RedHat-Satellite Python Scripts


#### Hosts Info

The script **redhat_satellite_hosts_info.py**  establishes a connection with Red Hat Satellite, extracts host information, and generates a CSV file named **hosts.csv**. The script has been tested successfully on Red Hat Satellite version 6.12.

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

Script Usage Syntax:

**python3 redhat_satellite_hosts_info.py --url https://your_host.example.redhat.com --username user**




#### Content View Info

The script **redhat_satellite_content_view_info.py**  establishes a connection with  Red Hat Satellite API to retrieve information about content views. Subsequently, it compiles this data and exports it to an Excel spreadsheet. Each sheet within the workbook corresponds to a specific content view, showcasing details such as content view version, latest update, activation key status, and repository listings. The name of the Excel file created will be **content_views_[Organization].xlsx**.

Script Usage Syntax:

**python3 redhat_satellite_content_view_info.py --username user --url https://your_host.example.redhat.com/ --organization "YOUR ORGANIZATION"**





#### Errata Info

The script **redhat_satellite_errata.py** extracts all RHSA, RHBA, and RHEA errata from Red Hat Satellite and saves them to a file named "errata.csv." It has been tested on Satellite 6.12. 

Script Usage Syntax:

**python3 redhat_satellite_errata.py  --url https://your_host.example.redhat.com --username user --type [RHSA,RHBA,RHEA,ALL]**


    Use RHSA to extract only RHSA (security) errata.
    Use RHBA to extract only RHBA (bugfix) errata.
    Use RHEA to extract only RHEA (enhancement) errata.
    Use ALL to extract all types of errata (RHSA, RHBA, RHEA).






#### Extra Info

To utilize the scripts, it's necessary to create an authentication token. You can achieve this by following these steps:

    Access Satellite's interface.
    Navigate to "Administer."
    Select the desired user.
    Choose "Personal Access Tokens."

