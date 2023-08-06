# MinuteInbox Temporary E-Mail
![GitHub Banner](https://repository-images.githubusercontent.com/380415345/e7d19f80-d64e-11eb-9c43-8a4af65c2a7a)
## Description
Create temporary e-mails and receive e-mails with MinuteInbox through python! It also parses the E-Mail adress MinuteInbox created for you; so you can directly access last and first name. And incase you needed it, it creates a company name out of them too 🎉

## Example
You'll be able to use this, just as in the following example:

```python
from minuteinbox import create_email, get_inbox
from time import sleep as s

# create an email
minuteinbox = create_email()
if minuteinbox:
	email = minuteinbox.get('email')
	first_name = minuteinbox.get('fname')
	last_name = minuteinbox.get('lname')
	company_name = minuteinbox.get('company')
	print('Current E-Mail: '+email+'\n'+'First & Last Name: '+first_name+' '+last_name+'\n'+'Company Name: '+company_name)


# get received email body
while True:
	inbox = get_inbox()
	if inbox != None:
		subject = inbox.get('subject')
		sender = inbox.get('sender')
		raw_body = inbox.get('raw_body') # raw text body
		clean_body = inbox.get('clean_body') # bs4 parsed body
		print('\nNew E-Mail titled: "'+subject+'", from: '+sender)
		print('\n'+'E-Mail Body:'+'\n'+clean_body)
		break
	s(3)
  ```
Output:
```
Current E-Mail: jahsiah.ayman@toiletkeys.net
First & Last Name: Jahsiah Ayman
Company Name: Ayja LLC

New E-Mail titled: "Meeting Minutes Defined", from: ahane 

E-Mail Body:
The meeting could be pretty intense and overwhelming for all members of the project. Therefore, it is natural that some of the participants are missing some details or slight information although they have taken personal notes on their device or paper. Kind Regards Copy Paste Emails
```

## Known Bugs
If there is weird special characters in the subject or the senders name, MinuteInbox tends to just send an empty response instead. That in return causes an error in this code. I've not found a bug fix for that yet.

## Disclaimer
I'm not associated in any way with MinuteInbox.com, if requested by them I will take down this repository. In this case please prove your Identity and send me an E-Mail. You can check my profile to find it.
