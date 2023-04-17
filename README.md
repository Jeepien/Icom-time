# Icom time
 Time sync handling for Icom transceivers 
 
 For the Raspberry Pi.  Waits for the top (:00) of the next minute and 
 writes the system time from the Pi to the Icom, including hour, minute; 
 timezone; month, day, and year.
 
 Tested on the IC 7300, but should work on other tranceivers using the same
 Icom CAT command set.

# Status:

# 17APR23
As an old-timer C coder, but newbie Python coder, this works as a proof of 
concept, but needs some work to make it truly useful.  For one thing, it 
does not currently check to see that the USB port open and writes are 
completed without error.  It seems to me that linux device ports are more
of an art than a science, so suggestions would be very welcome. I'm also
new to Github, so if I'm doing something goofy I'd like to know. Thanx.
   73, Gary AK2QJ
