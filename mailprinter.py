import imaplib
import base64
import os
import email
import getpass
import random
import time
import sys
import data.config as config

if len(sys.argv)>0:
    config.email_pass=getpass.getpass(prompt='Password: ', stream=None) 

while True:
    time.sleep(5)
    print('Checking...')
    mail = imaplib.IMAP4(config.email_server)
    mail.starttls()
    mail.login(config.email_user, config.email_pass)

    mail.select('INBOX')

    #Getting all Email-IDs and store it in data
    type, data = mail.search(None, 'UNSEEN')
    mail_ids = data[0]
    id_list = mail_ids.split()

    if len(data[0].split())>0:
        print('New Mails:')
    else:
        print('No new Mails')

    for num in data[0].split():
        typ, data = mail.fetch(num, '(RFC822)' )
        raw_email = data[0][1]# converts byte literal to string removing b''

        raw_email_string = ''
        
        try:
            raw_email_string=raw_email.decode('utf-8')
        except:
            raw_email_string=raw_email.decode('latin-1')

        email_message = email.message_from_string(raw_email_string)
        
        print('\t'+str(email_message.get_all('subject'))) 
        subject=str(email_message.get_all('subject')[0])
        date=str(email_message.get_all('date')[0])
        for part in email_message.walk():
            fileName = part.get_filename()
            if bool(fileName):
                if '.pdf' in fileName: 
                    printName=str(random.randrange(5,2**128))+'.pdf'
                    filePath = os.path.join(config.custom_temp, printName)
                    if not os.path.isfile(filePath) :
                        fp = open(filePath, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()
                        print('Downloaded "{file}" from email titled "{subject}" on {date}.'.format(file=fileName, subject=subject,date=date))
                        message='E-Mail title: {subject}\nReceived on: {date}\nFilename: {file} '.format(file=fileName, subject=subject,date=date)
                        os.system('lpr -P '+config.printer_name+' <<< "'+message+'"')
                        if not subject.split()[0].startswith('count:'):
                            os.system('lpr -P '+config.printer_name+' -o sides=two-sided-long-edge '+filePath)
                        else:
                            ct=str(subject.split()[0][6:])
                            os.system('lpr -#'+ct+' -P '+config.printer_name+' -o sides=two-sided-long-edge '+filePath)


                else:
                    print('File '+str(fileName)+' is not a pdf')
