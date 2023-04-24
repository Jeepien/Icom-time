# Icom time

 Time sync handling for Icom transceivers 
 
 For the Raspberry Pi.  
 The program contains one source file: Synctime7300.py 
 It waits for the top (:00) of the next minute and 
 writes the system time from the Pi to the Icom, including hour, minute; 
 timezone; month, day, and year.
 
 Tested on the IC 7300, but should work on other tranceivers using the same
 Icom CAT command set.
 
# Notes:

If you use this or a similar program to sync the transceiver, and want to 
be sure to keep the correct time(s) for daylight/standard transitions, set
the program to run one minute before the clock change time. For example, 
if you run it every day (and you're in the USA) set it to run at 01:59 
local time. That will set the time at exactly 02:00, which will assure that
the offcet to UTC will be correct.  If you run it once a week, do so at 
01:59 on Sunday mornings, as the US times always change on a Sunday.  

Of course you can also sync at every power-up (especially if your clock
batteries have gone bad) or at any other time.

# Status:

## 17APR23

As an old-timer C coder, but newbie Python coder, this works as a proof of 
concept, but needs some work to make it truly useful.  For one thing, it 
does not currently check to see that the USB port open and writes are 
completed without error.  It seems to me that linux device ports are more
of an art than a science, so suggestions would be very welcome. I'm also
new to Github, so if I'm doing something goofy I'd like to know. Thanx.
   73, Gary AK2QJ
