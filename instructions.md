## Instructions to boot

1. In folder codeklavier-extras/websocket-server
    python3 server.py --local —-reset (only use local if running both CKAR app AND CK from the same laptop)
2. In codeklavier folder: python3 codeklavier -p ckalculator
3. Open app CodeklaviAR (if using two laptops, make sure the app is configured to send to the local ip of SC computer. You can find this via the system pref or by <ifconfig> under the inet under en0 
4. In folder codeklavier-supercollider/ck_ar: osc_defs.sc (evaluate everything)


## How to use:
To make an axiom, the values must be within brackets and without a rule)
For example:
    (2 1 2)
    
To make a rule put the values of what you want changed, followed by the '.' and what it should become.
For example:
    (2.1 0 1)
    
You can also make 'no numbers' by in brackets making a comparison and adding a value to the True/False value.
For example:
    (5 > 4 [eval] + 3) essentialy this becomes (True + 3)
This translates to the 'N' token which removes the symbol

For tree operatons, the commands are as follows. Besides the dot, the other dunctions are only accesible in the context of a function (ostinato) figure. Please note the ostinato should have a change of 2 semitones.
dot: lowest A
create tree: C
drop tree: D, but short (make number first include evaluate!)
collect tree: D but long  (make number first include evaluate!)
next: F, but short
previous: F, but now tenuto
Eventually these operations will only exist in the context of defining a new function (with ostinato and a note change of 2 semitones). More to follow
transform: G
Change shape: A
