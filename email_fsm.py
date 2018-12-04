import smtplib

#input is true or false
#output is true or false should send email

counter = 0
state = 0


user = '459finalproject@gmail.com'                #Gmail login username
password = 'yasser459'        #Gmail login password
sender = '459finalproject@gmail.com'    #Email the message is sent from
to = '459finalproject@gmail.com'        #Email the password is sent to
msg = 'Your dog is in the camera'
def mail(dog_present):
	global counter, state
	
	if(counter > 0):
		counter = counter - 1
		state = 0

	elif(dog_present == False and counter == 0 and state == 0):
		state =0

	elif(dog_present == True and counter == 0 and state == 0):
		state = 1

	elif(dog_present == False and state == 1):
		state = 0

	elif(dog_present == True and state == 1):
		state = 2
		return True

	elif(dog_present == True and state == 2):
		state = 2

	elif(dog_present == False and state == 2):
		counter = 100
		state = 0

def send_email():
    global user, password, sender, to, msg
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(user,password)
    server.sendmail(sender,to,msg)