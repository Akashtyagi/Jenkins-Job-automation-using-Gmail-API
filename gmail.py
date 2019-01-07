# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 16:47:28 2018

@author: Akashtyagi
"""
'''
This script does the following:
- Go to Gmal inbox
- Find Email from the defined sender
- Extract Subject and full body of the mail from the sender
- Mark the messages as Read - so that they are not read again 
'''

'''
Before running this script, the user should get the authentication by following 
the link: https://developers.google.com/gmail/api/quickstart/python
Also, credentials.json should be saved in the same directory as this file
'''

# Importing required libraries
from googleapiclient import discovery
from googleapiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from bs4 import BeautifulSoup
import re
import time
import dateutil.parser as parser
from datetime import datetime
import datetime
import csv

flag = False

# Creating a storage.JSON file with authentication details
SCOPES = 'https://www.googleapis.com/auth/gmail.modify' # we are using modify and not readonly, as we will be marking the messages Read
store = file.Storage('storage.json') 
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

user_id =  'me'
label_id_one = 'INBOX'
label_id_two = 'UNREAD'
emailFrom = "akash tyagi <tyagiaakash001@gmail.com>"

# Getting all the unread messages from Inbox
# labelIds can be changed accordingly
unread_msgs = GMAIL.users().messages().list(userId='me',labelIds=[label_id_one, label_id_two]).execute()

# We get a dictonary. Now reading values for the key 'messages'
mssg_list = unread_msgs['messages']

print ("Total unread messages in inbox: ", str(len(mssg_list)))

final_list = [ ]
    
    
for mssg in mssg_list:
    temp_dict = { }
    m_id = mssg['id'] # get id of individual message
    message = GMAIL.users().messages().get(userId=user_id, id=m_id).execute() # fetch the message using API
    payld = message['payload'] # get payload of the message
    headr = payld['headers'] # get header of the payload
    
    for sender in headr:
        if sender['name'] == 'From':
            msg_from = sender['value']
            if str(msg_from) == str(emailFrom):
                temp_dict['Sender'] = msg_from
                flag = True
                print("From: "+msg_from)

                for one in headr: # getting the Subject
                    if one['name'] == 'Subject':
                        msg_subject = one['value']
                        temp_dict['Subject'] = msg_subject
                        print("Subject "+msg_subject)
                    else:
                        pass
                for two in headr: # getting the date
                    if two['name'] == 'Date':
                        msg_date = two['value']
                        date_parse = (parser.parse(msg_date))
                        m_date = (date_parse.date())
                        temp_dict['Date'] = str(m_date)
                        print(str(m_date))
                    else:
                        pass
                    
                temp_dict['Snippet'] = message['snippet'] # fetching message snippet
                
                try:
                    # Fetching message body
                    mssg_parts = payld['parts'] # fetching the message parts
                    part_one  = mssg_parts[0] # fetching first element of the part 
                    part_body = part_one['body'] # fetching body of the message
                    part_data = part_body['data'] # fetching data from the body
                    clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
                    clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
                    clean_two = base64.b64decode (bytes(clean_one, 'UTF-8')) # decoding from Base64 to UTF-8
                    soup = BeautifulSoup(clean_two , "lxml" )
                    mssg_body = soup.body()
                    # mssg_body is a readible form of message body
                    # depending on the end user's requirements, it can be further cleaned 
                    # using regex, beautiful soup, or any other method
                    temp_dict['Message_body'] = mssg_body
                except :
                    pass
                print (temp_dict)
                final_list.append(temp_dict) # This will create a dictonary item in the final list

                # This will mark the messagea as read
                GMAIL.users().messages().modify(userId=user_id, id=m_id,body={ 'removeLabelIds': ['UNREAD']}).execute()
                break
    break

print ("Total messaged retrived: ", str(len(final_list)))

if flag:
    action = re.search('##(.+?)##',str(mssg_body)).group(1)
    jobname = re.search('@@(.+?)@@',str(mssg_body)).group(1)
    print("Actions "+action)
    
    if action == 'trigger':
        print("Same")
        f = open(r"C:\Users\Akashtyagi\eclipse-workspace\Jenkins_API\src\test\java\job_properties.txt",'w')
        f.write(jobname)
        f.close()

        import os
        os.chdir(r'C:\Users\Akashtyagi\eclipse-workspace\Jenkins_API')
        os.startfile("script.bat")
        


'''

The final_list will have dictionary in the following format:

{	'Sender': '"email.com" <name@email.com>', 
	'Subject': 'Lorem ipsum dolor sit ametLorem ipsum dolor sit amet', 
	'Date': 'yyyy-mm-dd', 
	'Snippet': 'Lorem ipsum dolor sit amet'
	'Message_body': 'Lorem ipsum dolor sit amet'}


The dictionary can be exported as a .csv or into a databse
'''

#exporting the values as .csv
#with open('CSV_NAME.csv', 'w', encoding='utf-8', newline = '') as csvfile: 
#    fieldnames = ['Sender','Subject','Date','Snippet','Message_body']
#    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter = ',')
#    writer.writeheader()
#    for val in final_list:
#    	writer.writerow(val)



