import pyautogui
import time

import requests
from bs4 import BeautifulSoup
import pandas as pd



url = 'https://www.der-business-tipp.de/ort/name/id/' #change url
pageMaxNumber = 1000
mydata = None

for num in range(pageMaxNumber):
    pageUrl = url + str(num+1)
    print("pageUrl: ", pageUrl)
    page = requests.get(pageUrl)
    print(page)

    soup = BeautifulSoup(page.text, 'lxml')
    table1 = soup.find_all('table', {"class": "table"})[0]
    #print(table1)

    if(num == 0):
        headers = []
        #headerObj = table1.find_all('div', {"class": "row"})[0] #load headers
        for i in table1.find_all('th'):
            title = i.text #i.find('a').text
            headers.append(title)
            print(title)

        mydata = pd.DataFrame(columns = headers)

    print("body:")
    for j in table1.find('tbody').find_all('tr'): #load data [1:] , {"class": "box"}
        row_data = j.find_all('td')
        #print(j)
        row = [i.text.strip() for i in row_data]
        print("row: ",len(row))
        print(row)
        if(len(row) != 8):
            print("error: wrong colum number")
        else:
            length = len(mydata)
            mydata.loc[length] = row
    mydata.to_csv('test_contacts_data.csv', index=False) #change name of file

# Drop “Details” column
mydata.drop('Details', inplace=True, axis=1)

#export
mydata.to_csv('contacts_data.csv', index=False) #change name of file
