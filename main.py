import email_handler

service = email_handler.get_service()
user_id = 'me'
results = service.users().messages().list(userId=user_id, labelIds=['INBOX']).execute()
msg = results.get('messages', [])
print(msg)
for i in range(10):
    msg1 = msg[i]
    mg = service.users().messages().get(userId='me', id=msg1['id']).execute()
    print(mg['snippet'])