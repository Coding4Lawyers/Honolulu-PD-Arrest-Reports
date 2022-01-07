# Honolulu-PD-Arrest-Reports
 A program which scrapes and saves the HPD Arrest PDFs.
 
 ## TODO
 - Move saving of PDFs to an s3 bucket
 - Add in tests
 - Add in error notifications so someone can be notified if their website changes.

 ## Setup
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
 0 14 * * * /home/ubuntu/Honolulu-PD-Arrest-Reports/venv/bin/python /home/ubuntu/Honolulu-PD-Arrest-Reports/main.py > /home/ubuntu/Honolulu-PD-Arrest-Reports/cronlog.log 2>&1
 ```