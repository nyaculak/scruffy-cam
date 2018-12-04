int seen;
int counter;
int random;
bool send;
bool detected;
bool old;
int i;
active proctype email()
{
	seen=0
	counter = 0
	send=0
	i=1
	random = 1
	detected = 1
	do
	::(i>0) ->
		if
		:: (seen == 0 && detected == 1 && counter == 0) ->{seen = 1;send = 0}
		:: (seen == 0 && counter > 0) -> {counter = counter - 1}
		:: (seen == 1 && detected == 0) ->{seen = 0;send = 0}
		:: (seen == 1 && detected == 1) ->{seen = 2;send = 1}
		:: (seen == 2 && detected == 0) ->{seen = 0;send = 0; counter = 100}
		:: (seen == 2 && detected == 1) ->{seen = 2;send = 0}
		fi
		old = detected
		random = (12345*random+54321)%98765
		if
		::(random > 49382) -> {detected=1}
		::(random < 49383) -> {detected = 0}
		fi
	od
}

ltl invariant1 {<>((old==1 && detected==1)-><>(send==1))}
ltl invariant2 {<>((counter==100)-><>(counter==0))}