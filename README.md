# Honolulu-PD-Arrest-Reports
A program which scrapes and saves the Honolulu Police Department Arrest PDF at https://www.honolulupd.org/information/arrest-logs/
 
## TODO
1) Add in some catches for if the website is down or under construction
2) Add in some checks and an alert if the website is down or no ```<a>``` can be found.
3) Add in better logging
4) Right now we grab the first ```<a>``` but we should probably check to see if they have added a new pdf or for some reason they add two at once.

## Setup
Rename the passwords.example.py to passwords.py and add in credentials.
 ```
 git@github.com:Coding4Lawyers/Honolulu-PD-Arrest-Reports.git
 cd Honolulu-PD-Arrest-Reports
 python -m venv venv
 source venv/bin/activate
 pip install -r requirements.txt
 python main.py
 ```
Cronjob
 ```
 0 14 * * * /home/ubuntu/Honolulu-PD-Arrest-Reports/venv/bin/python /home/ubuntu/Honolulu-PD-Arrest-Reports/main.py >> /home/ubuntu/Honolulu-PD-Arrest-Reports/cronlog.log 2>&1

 ```