import smtplib
 
to = '22.22@22.com'
gmail_user = '22222@gmail.com'
gmail_pwd = '22222'
smtpserver = smtplib.SMTP("smtp.gmail.com",587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo
smtpserver.login(gmail_user, gmail_pwd)
header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:testing \n'
print header
msg = header + '\n this is test msg from mkyong.com \n\n'
print smtpserver.sendmail("tejas.tank@microsoft.com", to, msg)
print 'done!'
smtpserver.close()
