#!/usr/bin/python

import math
import struct
import alsaaudio,time

inp=alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)

inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

inp.setperiodsize(160)
print inp.cardname()

time.sleep(5)
while True:
	try:
		I,data=inp.read()
 		count = len(data)/2
  		format = "%dh"%(count)
    		shorts = struct.unpack( format, data )

		# iterate over the block.
		sum_squares = 0.0
		for sample in shorts:
		# sample is a signed short in +/- 32768. 
		# normalize it to 1.0
			n = sample * (1.0/3  
			sum_squares += n*n
		if count>0 :
			if math.sqrt(sum_squares/count)>100:
				print math.sqrt(sum_squares/count)
		#time.sleep(0.001)
	except:	
		
		print "error"
		inp.close()
		time.sleep(2)
		try:
			inp.close()
			inp=alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)

			inp.setchannels(1)
			inp.setrate(8000)
			inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

			inp.setperiodsize(160)
		except:
			print "not yet"
