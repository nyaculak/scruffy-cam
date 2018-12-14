// store last 3 inputs to the system
bool ppdetected = false;
bool pdetected = false;
bool detected = false;

// output
bool send_email;

// state
int state = 0;

active proctype email() {
    printf("\n");
    int bound = 100;
    do :: (bound > 0) ->
        // Environment: nondeterministic FSM
        if
        :: true -> 
            ppdetected = pdetected;
            pdetected = detected;
            detected = 0;
        :: true -> 
            ppdetected = pdetected;
            pdetected = detected;
            detected = 1;
        fi;
        printf("%d %d %d\n", ppdetected, pdetected, detected);

        // System: deterministic FSM
        if
        :: (state == 0 && !detected) ->
            state = 0;
        :: (state == 0 && detected) ->
            state = 1;
        :: (state == 1 && !detected) ->
            state = 0;
        :: (state == 1 && detected) ->
            state = 2;
            send_email = true;
            printf("\tSend email\n");
        :: (state == 2 && detected) ->
            state = 2;
            send_email = false;
        :: (state == 2 && !detected) ->
            state = 0;
            send_email = false;
        fi;

        // Label to specify the "return" part of the FSM function
        RETURN:
        bound = bound - 1;
    od;
    printf("End Simulation\n");
}

// Test the output of the system based only on the last 3 inputs

// If any of the last two inputs are misses, no email should be sent
// ltl email_fails_at_zero_or_one {[]( (!detected || !pdetected) && email@RETURN -> !send_email )}

// If the last two inputs are hits, but the one before is a miss, the email should be sent
// ltl email_sends_at_exactly_two {[] (!ppdetected && pdetected && detected && email@RETURN -> send_email)}

// If the last three or more inputs were hits, another email should not be sent
// ltl email_fails_at_three_or_more {[] (ppdetected && email@RETURN -> !send_email)}

// These logical implications can be combined into a single logical equivalence
ltl invariant {[]( 
    !ppdetected && pdetected && detected && email@RETURN <-> send_email && email@RETURN
)}
