#! /usr/bin/python3

#Synctime7300

#=======================================================================
# Copyright 2022, 2023 Gary P. Novosielski
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#=======================================================================

# This script reads the system time and date for one minute in
#  the future, which is the time we will set, then waits
#  till HH:MM:00, and sends that time, date, and zone
#  to the IC-7300's clock.

# by Gary, AK2QJ
# inspired by original idea of Kevin, KB8RLW 
#
# This will set the clock properly even if the settings have
#  been completely toasted.
#
# The radio's clock keeps local time but will display UTC time
#  if the clock digits are touched on the touchscreen.  If your
#  localization time zone is correctly set, this script will keep
#  the UTC zone offset corrected for daylight or standard time,
#  presuming you use local time.  UTC is an option as well, which
#  will set both clocks to UTC. See use_utc in the next section.
#
# If you exec this once per day and are using local time, 
#  do so at 01:59.  This will cause it to set at 02:00:00, 
#  which is exactly when US clock changes, if any, happen.

# Initialize some stuff.
#
#  These 3 lines are installation-dependent:
baudrate = 19200  # set this to match radio, or vice versa
serialport = '/dev/ttyUSB1' # CAT port, probably correct, but check.
use_utc = False # True for UTC, False for local time

import time
import serial

preamble = b'\xFE\xFE\x94\xE0\x1A\x05\x00' # Commands start with this
endrec   = b'\xFD'                         #  and end with this

# The 3 CAT records preloaded with subcmd codes
# These are string values but will be converted to
# hexadecimal (actually BCD) when sent by syncout().

catdate = ['94']    #\
cattime = ['95']     #= Ref: Icom IC-7300 Full Manual, 
catzone = ['96']    #/       A7292-4EX-8; pp. 19-2 ff.


# Do what we can before time-critical parts begin

# Open the serial port
ser = serial.Serial(serialport, baudrate)

# define the output function
# This is where the string values get translated to hex bytes
#  and sent out the USB port.
def syncout(record):
    '''Write a record, wrapped in proper control codes.'''
    
    ser.write(preamble)       # same for all commands
    
    for i in range(len(record)):  # then for each byte:
        ser.write(bytes([int(record[i], 16)]))  # write as a byte, i.e., hex or BCD
        
    ser.write(endrec)         # end of command
        
    # Command sent
    time.sleep(0.100) # 100 ms, because why not.
    return None
# end def

#=========================== Waste no time in this section =============== 
# Okay, here we go...
# Get the time a minute in the future into the t time struct
#  by adding 60 to the current ticks.

ticks = time.time() # Freeze time, in seconds since 1969

# Allow time.???time to handle boundary conditions neatly
#  even if run at 23:59 on Dec 31st.
#
if use_utc:
    t = time.gmtime(ticks + 60.) # Store values for a minute from now
else:
    t = time.localtime(ticks + 60.) # Store values for a minute from now
#
# Assemble the time record
#
cattime.append(str(t.tm_hour))  #hour    HH
cattime.append(str(t.tm_min))   #minute  MM
# When this is sent...          #seconds 00.
#========================= End of time-critical section =================

# Wait for the top of minute by sleeping for
#  the remainder of the current minute.
# This works well because Python's mod (%) returns
#  a float, which retains fractions of a second.
time.sleep(60.0 - (ticks % 60))  # ZZZZZZzzzzzzzzzz
# Then write the time record, to set :00 at that moment.
syncout(cattime)
# Time has been set.

#
# Assemble the date record, using the same instant frozen in t.
#
catdate.append(str(t.tm_year // 100))  #century CC  note int division
catdate.append(str(t.tm_year % 100))   #year    YY
catdate.append(str(t.tm_mon))          #month   MM
catdate.append(str(t.tm_mday))         #day     DD

# Time zone needs a little work:
# Convert UTC offset into time zone value for Icom.
# Change seconds-east-of-Greenwich to hours-east-of-Greenwich
# e.g., US Eastern Time will be -5, or if daylight time, -4.
# If using UTC, tm_gmtoff will be 0 as expected.
#
tz = t.tm_gmtoff // 3600  # more integer division

# Separate the sign the way the Icom likes it
#
if tz < 0:
    sign = '1'   # negative: Western Hemisphere
    tz = abs(tz) # then remove sign from tz
else:
    sign = '0'   # non-negative: Eastern Hemisphere
    
# Get minutes for fractional-hour time zones.
# The IC-7300 can only be set to nearest 5 minutes.
# This will be 00 for normal full-hour time zones.
#
tzm = (abs(t.tm_gmtoff) % 3600) // 60 #  mod abs seconds to one hour, then // 60 for minutes

#
# Assemble the zone record.
#
catzone.append(str(tz))  # hours offset
catzone.append(str(tzm)) # minutes offset
catzone.append(sign)     # sign of the offset. I think.  I have not researched this in depth.

# Write remaining records. 

syncout(catdate)
syncout(catzone)
    
ser.close()  # finished with device

# ...and we're all done.  Bye!
