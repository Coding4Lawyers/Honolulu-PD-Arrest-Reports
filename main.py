import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import pytz
import time
import boto3
import passwords


def getPDF():
    #Sends the request to get the webpage where the PDF links are
    url = 'https://www.honolulupd.org/information/arrest-logs/'
    headers = \
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    #Get the div with all the anchor tags and then grab the first link which should be the most recent days link.
    arrestdiv = soup.find('ul', attrs={'class': 'hpd-arrest-logs'})
    atag = arrestdiv.find('a')

    #Call the downloadPDF function and pass to it the url of the top <a> which should be the link we want.
    return downloadPDF(atag['href'])

def downloadPDF(url):
    #Do some testing to make sure folder exists

    #Make the request to the url with the PDF we want
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    r = requests.get(url, headers=headers, stream=True)
    #print("Status Code",r.status_code)
    if(r.status_code != 200):
        print("Error Status Code",r.status_code)
        return False
    if(len(r.content) < 10000):
        print("Error in length of PDF",len(r.content))
        return False

    pdffilename = url[54:]

    #Write the data from the request to a PDF file

    #Write file to s3
    writeFileToS3(r.content,passwords.aws_bucket_name,pdffilename)

    #Write file locally
    #savePDFLocally(r.content,pdffilename)

    return True

def savePDFLocally(content,pdfname):
    foldername = "ArrestLogPDFs"
    folder_exists = os.path.isdir(foldername)
    # If folder doesn't exist, then create it.
    if folder_exists != True:
        os.makedirs(foldername)

    pdfname = foldername + "/" + pdfname
    pdf = open(pdfname, 'wb')
    pdf.write(content)
    pdf.close()
def writeFileToS3(content, bucket, filename):
    #Upload content from the request response to s3 so we never have to save the file locally.

    # Upload the file
    session = boto3.Session(
                             aws_access_key_id=passwords.aws_access_key_id,
                             aws_secret_access_key=passwords.aws_secret_access_key
                             )
    s3 = session.resource('s3')
    object = s3.Object(bucket, filename)
    result = object.put(Body=content)

    if(result['ResponseMetadata']['HTTPStatusCode'] != 200):
        print("Error with S3")
        print(result)

if __name__ == '__main__':
    x = 0
    try:
        #We had problems with it not downloading right so now we try 5 times.
        while x < 5:
            print("Attempting to scrape Arrest Logs",datetime.now(pytz.timezone('Pacific/Honolulu')))
            success = getPDF()

            time.sleep(2)
            if(success == True):
                print("Successful")
                break
            else:
                print("Failure Attempting Again",x)
            x+=1

    except Exception as e:
        print("Failure:")
        print(e)