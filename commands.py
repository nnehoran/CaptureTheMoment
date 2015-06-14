"""
selectPressed	(none)	CCE pressed.
selectReleased	(none)	CCE released.
pushUpPressed	(none)	CCE slide UP pressed.
pushUpReleased	(none)	CCE slide UP released.
pushRightPressed	(none)	CCE slide RIGHT pressed.
pushRightReleased	(none)	CCE slide RIGHT released.
pushDownPressed	(none)	CCE slide DOWN pressed.
pushDownReleased	(none)	CCE slide DOWN released.
pushLeftPressed	(none)	CCE slide LEFT pressed.
pushLeftReleased	(none)	CCE slide LEFT released.
cceRotate	change	CCE rotation. Clockwise rotation is represented as a positive number of steps; Counterclockwise rotation is represented as a negative number of steps.
cceBackPressed	(none)	CCE BACK function button pressed.
cceBackReleased	(none)	CCE BACK function button released.
favoritePressed	(none)	CCE FAVORITE function button pressed.
favoriteReleased	(none)	CCE FAVORITE function button released.


touchpadAreaTouched	(none)	The touchpad area or the touchpad buttons has been touched.
touchpadAreaPressed	(none)	The touchpad surface is clicked to indicate a selection.
swipeUp	touches	The touchpad detected an UP gesture. The number of finger touches is returned (either 1 or 2).
swipeRight	touches	The touchpad detected a RIGHT gesture. The number of finger touches is returned (either 1 or 2).
swipeDown	touches	The touchpad detected a DOWN gesture. The number of finger touches is returned (either 1 or 2).
swipeLeft	touches	The touchpad detected a LEFT gesture. The number of finger touches is returned (either 1 or 2).
touchRotate	change	The touchpad detected a ROTATION gesture. Clockwise rotation is represented as a positive number of steps; Counterclockwise rotation is represented as a negative number of steps.
touchZoom	direction	The touchpad detected a PINCH gesture. A pinch-open gesture is represented as a positive direction; A pinch-closed gesture is represented as a negative direction.
touchHold	touches	The touchpad detected a touch and HOLD. The hold gesture occurs when a touch is active and no motion is detected for more than 1 second. The number of finger touches is returned (either 1 or 2).
touchAt	x
y
touches	Touch coordinates are periodically reported when the values change. The x-axis and y-axis coordinate values are reported with the origin at the top-left corner of the touchpad. The number of finger touches is returned (either 1 or 2). Coordinates for the barycenter of multiple touches is used in case of multiple touches. Coordinate values are bound from 0 to 1024. Expected values are returned from 90-320 on the x-axis and 60-400 on the y-axis. Actual values may vary between touchpads depending on calibration of the device.
touchpadBackTouched	(none)	The touchpad detected a touch on the BACK touch area.
touchpadBackPressed	(none)	The touchpad surface is clicked on the BACK touch icon.
touchpadMediaTouched	(none)	The touchpad detected a touch on the MEDIA touch icon.
touchpadMediaPressed	(none)	The touchpad surface is clicked on the MEDIA touch icon.
touchpadFavoriteTouched	(none)	The touchpad detected a touch on the FAVORITE touch icon.
touchpadFavoritePressed	(none)	The touchpad surface is clicked on the FAVORITE touch icon.
"""
import os
import sys
import time
import copy
import threading
import zerorpc

import cv2

#from goprohero import GoProHero


#class DisplayThread(threading.Thread):
class DisplayThread(threading.Thread):

     def __init__(self, cmmds):
        #threading.Thread.__init__(self)
        self.cmmds = cmmds
        self.lastvideoRecording = False
        self.lasttakephoto = False
        self.phototime = 0
        self.lastframe = None
        if not os.path.exists("images"):
           os.makedirs("images")
        if not os.path.exists("videos"):
           os.makedirs("videos")

     def run(self):

	while(True):
	    # Capture frame-by-frame
	    ret, frame = self.cmmds.camera.read()
            #print "image read"
            #cv2.imwrite("junk.jpg", frame)

	    # Display the resulting frame
            if self.cmmds.takephoto and self.lastframe != None:
               font = cv2.FONT_HERSHEY_SIMPLEX
               copyframe = copy.copy(self.lastframe)
               cv2.putText(copyframe, "Photo taken", (32, 32), font, 1, (0, 255, 0), 2) 
	       cv2.imshow('frame', copyframe)
            else:
               copyframe = copy.copy(frame)
               if self.cmmds.videoRecording:
                  cv2.circle(copyframe, (20,20), 10, (0,0,255), -1)
                  #font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8)
                  font = cv2.FONT_HERSHEY_SIMPLEX
                  cv2.putText(copyframe, "Recording", (32, 32), font, 1, (0, 0, 255), 2) 
	       cv2.imshow('frame', copyframe)
            #print "image showed"

            #print "videomode: %s, videorecording: %s, lastvideoRecording: %s" % \
            #      (self.cmmds.videomode, self.cmmds.videoRecording, self.lastvideoRecording)
            #print "takephoto: %s, lasttakephoto:%s" % (self.cmmds.takephoto, self.lasttakephoto)
            ts = time.strftime("%d-%m-%Y-%H-%M-%S")
           
            # Take the photo 
            if self.lasttakephoto == False and self.cmmds.takephoto:
               print "taking photo at %s" % ts
               fname = "images/%s.jpg" % ts
               lt, ln = self.cmmds.get_position()   
               font = cv2.FONT_HERSHEY_SIMPLEX
               cv2.putText(frame, "%s %s" % (lt, ln), (32, 70), font, 1, (171, 222, 255), 2) 
               cv2.imwrite(fname, frame)
               #self.cmmds.takephoto = False
               self.phototime = time.time() 
               self.lastframe = frame

            # Display the same photo for some time 
            if self.lasttakephoto and self.cmmds.takephoto:
               t1 = time.time()
               #print "photo_time:%f current_time: %f" % (self.phototime, t1)
               if (t1 - self.phototime) > 1:
                  self.cmmds.takephoto = False

            # video starting
            if self.lastvideoRecording == False and self.cmmds.videoRecording:
               print "starting video at %s" % ts
               fname = "videos/%s.mov" % ts
               fourcc = cv2.cv.CV_FOURCC(*'mp4v')
               w=int(self.cmmds.camera.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH ))
               h=int(self.cmmds.camera.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT ))
               videof = cv2.VideoWriter(fname, fourcc, 20.0, (w,h))
               videof.write(frame)
           
            # video running
            if self.lastvideoRecording and self.cmmds.videoRecording:
               videof.write(frame)
                
            # video ending
            if self.lastvideoRecording and self.cmmds.videoRecording == False:
               print "ending video at %s" % ts
               fname = "%s.avi" % ts
               videof.write(frame)
               videof.release()

            self.lastvideoRecording = self.cmmds.videoRecording
            self.lasttakephoto = self.cmmds.takephoto

	    if cv2.waitKey(1) & 0xFF == ord('q'):
		break

class CommandThread(threading.Thread):

     def __init__(self, cmmds):
        threading.Thread.__init__(self)
        self.cmmds = cmmds

     def run(self):
        self.cmmds.cceFavoriteReleased("cceFavoriteReleased")
	self.cmmds.selectReleased("selectReleased")
        time.sleep(5)
        i = 0
        while True:
             time.sleep(1.1)
	     self.cmmds.selectReleased("selectReleased")
             if (i%4 == 0):
                self.cmmds.cceFavoriteReleased("cceFavoriteReleased")
             i = i +1
 

class CommandControl:
	def __init__(self):
		self.name = "command-control"
                self.cmode = "mbpro"
                self.videomode = False
                self.videoRecording = False
                self.takephoto = False

                if self.cmode == "mbpro":
                   self.camera = cv2.VideoCapture(0)
                else:
		   self.camera = GoProHero(password='kesav123')
		   self.camera.command('power', 'on')
		   print(self.camera.status())

                self.rpc1 = zerorpc.Client()
                self.rpc1.connect("tcp://127.0.0.1:4242")

        def startDisplay(self):
                # start the display thread
                self.displaythread = DisplayThread(self)
                self.displaythread.run()
 
	def log(self, message):
		print("%s" % message)

        def get_position(self):
            import auto_snap
            data = auto_snap.readVehicleData(2)
            return (data['GPS_Latitude'], data['GPS_Longitude'])

	# define all commands of rotary controller and touchpad

	# Rotary controller commands
	def selectPressed(self, cmd=""):
		self.log("Command: %s" % cmd)

	def selectReleased(self, cmd=""):
		self.log("Command: %s" % cmd)

		if self.videomode:
                   self.videoRecording = not self.videoRecording
                else:
                   self.takephoto = True

                if self.cmode == "mbpro":
                   pass
                else:
		   self.camera.command('record', 'on')
                   
	def pushUpPressed(self, cmd=""):
		self.log("Command: %s" % cmd)

	def pushUpReleased(self, cmd=""):
		self.log("Commansd: %s" % cmd)

	def pushRightPressed(self, cmd=""):
		self.log("Command: %s" % cmd)

	def pushRightReleased(self, cmd=""):
		self.log("Command: %s" % cmd)

	def pushDownPressed(self, cmd=""):
		self.log("Command: %s" % cmd)

	def pushDownReleased(self, cmd=""):
		self.log("Command: %s" % cmd)

	def pushRightPressed(self, cmd=""):
		self.log("Command: %s" % cmd)

	def pushRightReleased(self, cmd=""):
		self.log("Command: %s" % cmd)

	def cceRotate(self, cmd="", change=0):
		self.log("Command: %s change: %s" % (cmd, change))

	def cceBackPressed(self, cmd=""):
		self.log("Command: %s" % cmd)

	def cceBackReleased(self, cmd=""):
		self.log("Command: %s" % cmd)

	def cceFavoritePressed(self, cmd=""):
		self.log("Command: %s" % cmd)

	def cceFavoriteReleased(self, cmd=""):
		self.log("Command: %s" % cmd)
		self.videomode = not self.videomode
                self.videoRecording = False

	# Touchpad controls

	def touchpadAreaTouched(self, cmd=""):
		self.log("Command: %s" % cmd)

	def touchpadAreaPressed(self, cmd=""):
		self.log("Command: %s" % cmd)

	def swipeUp(self, cmd="", touches=1):
		self.log("Command: %s touches:%d" % (cmd, touches))

	def swipeLeft(self, cmd="", touches=1):
		self.log("Command: %s touches:%d" % (cmd, touches))
                self.rpc1.previous()

	def swipeRight(self, cmd="", touches=1):
		self.log("Command: %s touches:%d" % (cmd, touches))
                self.rpc1.next()

	def swipeDown(self, cmd="", touches=1):
		self.log("Command: %s touches:%d" % (cmd, touches))

	def touchHold(self, cmd="", touches=0):
		self.log("Command: %s touches:%d" % (cmd, touches))

	def touchRotate(self, cmd="", change=0):
		self.log("Command: %s change: %d" % (cmd, change))

	def touchZoom(self, cmd="", direction=0):
		self.log("Command: %s" % cmd)

	def touchAt(self, cmd="", touches=0, x=0, y=0):
		self.log("Command: %s touches: %d x: %d y: %d" % (cmd, touches, x, y))

	def touchpadBackTouched(self, cmd=""):
		self.log("Command: %s" % cmd)

	def touchpadBackPressed(self, cmd=""):
		self.log("Command: %s" % cmd)

	def touchpadMediaTouched(self, cmd=""):
		self.log("Command: %s" % cmd)

	def touchpadMediaPressed(self, cmd=""):
		self.log("Command: %s" % cmd)

	def touchpadFavoriteTouched(self, cmd=""):
		self.log("Command: %s" % cmd)

	def touchpadFavoritePressed(self, cmd=""):
		self.log("Command: %s" % cmd)

        def quickphoto(self, cmd=""):
		self.log("Command: %s" % cmd)
                if self.videoRecording:
                   return
                lastvideomode = self.videomode
                self.videomode = False
                self.takephoto = True
                time.sleep(0.1)
                self.videomode = lastvideomode

def test_command_control():
	c = CommandControl()
        cthread = CommandThread(c)
        cthread.start()
        c.startDisplay()


def main():
	test_command_control()


if __name__ == '__main__':
	main()
