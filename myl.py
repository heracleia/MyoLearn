# -*- coding: utf-8 -*-

from socketIO_client import SocketIO, BaseNamespace
import myo as libmyo
import numpy as np
import threading
import time

class MyoNamespace(BaseNamespace):
	def on_connect(self):
		print 'Connected to http://localhost:3000'
		
	def on_ping_myo(self):
		myo_sock.emit('confirm');
		
def stream():
	#Initialize
	libmyo.init() 
	feed = libmyo.device_listener.Feed()
	hub = libmyo.Hub()
	hub.run(1000, feed)
	myo = feed.wait_for_single_device()

	#Continuously collect and emit data
	while 1:
		try:
			gyro = myo.gyroscope
			accel = myo.acceleration
			myo_sock.emit('data', [time.clock(), gyro.x, gyro.y, gyro.z, accel.x, accel.y, accel.z])
			time.sleep(0.02)
		except KeyboardInterrupt:
			break
		except:
			print 'Unexpected error'
			
	hub.shutdown()

#Start data collection as separate thread
socketIO = SocketIO('localhost', 3000)
myo_sock = socketIO.define(MyoNamespace, '/myo_namespace')
socketIO.wait(seconds=1)
thread = threading.Thread(target=stream)
thread.daemon=True
thread.start()
socketIO.wait();