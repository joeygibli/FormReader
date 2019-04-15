import argparse
import cv2
from PIL import Image
import pytesseract as pyt

cropRegions = []
clones = []
cropping = False

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

# load the image, clone it, and setup the mouse callback function
original = cv2.imread(args["image"])
image = cv2.imread(args["image"])
clones.append(image.copy())
cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 1000,1000)


def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables, necessary on writes [[why not sure]]
 	global cropping
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		clones.append(image.copy())
		cropRegions.append((x, y))
		cropping = True
 
	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		if cropping:
			cropRegions.append((x, y))
			cropping = False
	 
			# draw a rectangle around the region of interest
			cv2.rectangle(image, cropRegions[len(cropRegions)-2], cropRegions[len(cropRegions)-1], (0, 0, 255), 1)
			cv2.imshow("image", image)
 
 
# keep looping until the 'q' key is pressed
cv2.setMouseCallback("image", click_and_crop)

while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'r' key is pressed, reset the cropping region
	if key == ord("r"):
		if cropping:
			cropRegions.pop()
			cropping = False
		else:
			cropRegions.pop()
			cropRegions.pop()
		undid = clones.pop()
		image = undid
	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break

	elif key == ord("q"):
		cv2.destroyAllWindows()
		quit()
 
# if there are two reference points, then crop the region of interest
# from teh image and display it
if len(cropRegions) >= 2:
	assert len(cropRegions)%2 == 0 # ensure that we have pairs of points for rectangles

	numImages = len(cropRegions)/2
	for i in range(numImages):
		y0, y1 = cropRegions[2*i][1], cropRegions[2*i+1][1]
		x0, x1 = cropRegions[2*i][0], cropRegions[2*i+1][0]

		if y0 == y1 or x0 == x1: # size cannot be 0 in either dimension
			break

		# adjust ordering of variables 
		if y0 > y1:
			tmp = y0
			y0 = y1
			y1 = tmp
		if x0 > x1:
			tmp = x0
			x0 = x1
			x1 = tmp

		cropped = original[y0:y1, x0:x1]
		cv2.imwrite("Cropped/Crop"+str(i)+".png", cropped)

	for i in range(numImages):
		image_file = Image.open('Cropped/Crop'+str(i)+'.png')
		image_file = image_file.convert('1', dither=Image.NONE)
		print(pyt.image_to_string(image_file))

cv2.waitKey(0) 
# close all open windows
cv2.destroyAllWindows()