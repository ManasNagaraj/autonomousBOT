

import cv2
import numpy as np


cap = cv2.VideoCapture(0)

def adjust_gamma(image, gamma=5.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")

	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)


while True:
    __,frame = cap.read()
    cv2.imshow("b4gammacorrection",frame)
    image = adjust_gamma(frame)
    cv2.imshow("gamma correction",image)
    key = cv2.waitKey(1)
    if key == 27:
        break


cv2.destroyAllWindows()    
