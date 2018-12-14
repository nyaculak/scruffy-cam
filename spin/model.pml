// input
bool prev_detected = false;
bool detected = false;

// output
bool send_email;

// state
int state = 0;

// variables
int counter = 0;

active proctype email() {
    printf("\n");
    int bound = 10;
    do :: (bound > 0) ->
        if
        :: true -> 
            prev_detected = detected;
            detected = 0;
        :: true -> 
            prev_detected = detected;
            detected = 1;
        fi;
        printf("Detected: %d   (Prev) %d \n", detected, prev_detected)

        if
        :: (state == 0 && counter > 0) ->
            counter = counter - 1;
            state = 0;
        :: (state == 0 && counter == 0 && !detected) ->
            state = 0;
        :: (state == 0 && counter == 0 && detected) ->
            state = 1;
        :: (state == 1 && !detected) ->
            state = 0;
        :: (state == 1 && detected) ->
            state = 2
            SENDING:
            send_email = true;
            printf("\tSend email\n");
        :: (state == 2 && detected) ->
            state = 2
            send_email = false;
        :: (state == 2 && !detected) ->
            counter = 10
            state = 0
            send_email = false;
        fi;
        bound = bound - 1;
    od;
    printf("End Simulation\n");
}

// ltl invar { []((prev_detected && detected) -> <>(send_email)) }
// ltl invariant2 {<>(counter==10) -> <>(counter==2)}
ltl invariant { [] (email@SENDING -> (prev_detected && detected)) }
