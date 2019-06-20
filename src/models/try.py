import smtplib
server = smtplib.SMTP

SERVER = "smtp.example.com"
FROM = "ivan.botev@innvotek.com"
TO = ["listOfEmails"] # must be a list

SUBJECT = "Subject"
TEXT = "Your Text"

# Prepare actual message
message = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

# Send the mail
server = smtplib.SMTP(SERVER)
server.sendmail(FROM, TO, message)
server.quit()
