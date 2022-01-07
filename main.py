import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import pytz
import platform

#TODO: 1) Add in some catches for if the website is down or under construction
#TODO: 2) Add in some checks and an alert if the website is down or no <a> can be found.
#TODO: 3) Build a PDF Parser
#TODO: 4) Move the file saving to s3 so we don't run out of space.

def getPDF():
    #Sends the request to get the webpage where the PDF links are
    url = 'https://www.honolulupd.org/information/arrest-logs/'
    headers = \
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    #Get the div with all the anchor tags and then grab the first link which should be the most recent days link.
    arrestdiv = soup.find('div', attrs={'class': 'entry-content'})
    atag = arrestdiv.find('a')

    #Call the downloadPDF function and pass to it the url of the top <a> which should be the link we want.
    downloadPDF(atag['href'])

def downloadPDF(url):
    #Do some testing to make sure folder exists

    if(platform.system() == 'Windows'):
        linuxdirectory = '/home/ubuntu/Honolulu-PD-Arrest-Reports/'
    else:
        linuxdirectory = ""

    foldername = linuxdirectory + "ArrestLogPDFs"
    folder_exists = os.path.isdir(foldername)
    # If folder doesn't exist, then create it.
    if folder_exists != True:
        os.makedirs(foldername)

    #Make the request to the url with the PDF we want
    r = requests.get(url, stream=True)

    #Create a file name that consists of the a timestamp of when we downloaded it and the name of the PDF from the url
    #Seperate the two parts with @@@
    #This way we can in theory build something later on to parse the timestamp from the file name if we need to.
    timestamp = datetime.now(pytz.timezone('Pacific/Honolulu'))
    datetimestamp = timestamp.strftime('%Y-%m-%d')
    pdfname = foldername + '/' + datetimestamp + "@@@" + url[54:]

    #Write the data from the request to a PDF file
    pdf = open(pdfname, 'wb')
    pdf.write(r.content)
    pdf.close()

if __name__ == '__main__':
    try:
        print("Attempting to scrape Arrest Logs",datetime.now(pytz.timezone('Pacific/Honolulu')))
        getPDF()
        print("Successful")
    except Exception as e:
        print(e)