import imaplib
import re


user = 'YOUR MAIL ID'
pwd = 'PASSWORD'

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(user, pwd)
mail.list()
# Out: list of "folders" aka labels in gmail.
mail.select("inbox")  # connect to inbox.


def sendMails(address):
    result, data = mail.search(None, '(FROM '+'"'+address+'")')

    ids = data[0]  # data is a list.
    id_list = ids.split()  # ids is a space separated string
    latest_email_id = id_list[0]  # get the latest

    # fetch the email body (RFC822) for the given ID
    result, data = mail.fetch(latest_email_id, "(RFC822)")

    # here's the body, which is raw text of the whole email
    raw_email = data[0][1]
    # including headers and alternate payloads

    index_start1 = raw_email.index(b'Subject')
    index_end1 = index_start1 + 40          #Chnage the value 40 according to your preferences.
    index_start2 = raw_email.index(b'ltr')
    index_end2 = len(raw_email)

    subject = raw_email[index_start1:index_end1]
    body = raw_email[index_start2:index_end2]

    body = body.strip(b'ltr\">')
    subject = subject.strip(b'b\'Subject: ')
    body_end = body.index(b'</')
    subject_end = subject.index(b'\r')

    print('-------FROM '+address+'-------\n\n')
    print("Subject: ", subject[0:index_end1], '\n\n')
    print("Body: ", body[0:body_end])


listOfMails = ['MAIL1@GMAIL.COM',
               'MAIL2@GMAIL.COM', 'MAIL3@GMAIL.COM', 'MAIL4@GMAIL.COM', 'MAIL5@GMAIL.COM']

for addresses in listOfMails:
    sendMails(addresses)

mail.logout()
