#input is true or false
#output is true or false should send email

global counter
global state
counter = 0
state = 0


def mail(dog_present):
	
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




	

