#!/usr/bin/env python
# -*- coding: utf-8 -*-
#mirlight.test by grizz - Witek Firlej http://grizz.pl
#ver. 0.1 2010.01.26

import serial
#conf:
port = 1
data = [128, 10,	10,	10,	10,	10,	10,	10,	10,	10,	10,	10,	10,	10,	10,	10,	10,	10,	10,	10,	10,	10,	10,	10,	10,	56]

ser = serial.Serial(port, 38400, timeout=0)

print data
kod = ""
for x in data:
	kod += chr(x)
ser.write(kod)

