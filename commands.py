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


class CommandControl:
	def __init__(self):
		self.name = "command-control"

	def log(self, message):
		print("%s" % message)

	# define all commands of rotary controller and touchpad

	# Rotary controller commands
	def selectPressed(self, cmd=""):
		self.log("Command: %s" % cmd)

	def selectReleased(self, cmd=""):
		self.log("Command: %s" % cmd)

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

	def favoritePressed(self, cmd=""):
		self.log("Command: %s" % cmd)

	def favoriteReleased(self, cmd=""):
		self.log("Command: %s" % cmd)

	# Touchpad controls

	def touchpadAreaTouched(self, cmd=""):
		self.log("Command: %s" % cmd)

	def touchpadAreaPressed(self, cmd=""):
		self.log("Command: %s" % cmd)

	def swipeUp(self, cmd="", touches=1):
		self.log("Command: %s touches:%d" % (cmd, touches))

	def swipeLeft(self, cmd="", touches=1):
		self.log("Command: %s touches:%d" % (cmd, touches))

	def swipeRight(self, cmd="", touches=1):
		self.log("Command: %s touches:%d" % (cmd, touches))

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


def test_command_control():
	c = CommandControl()
	c.selectPressed("selectPressed")


def main():
	test_command_control()


if __name__ == '__main__':
	main()
