import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob

nx = 9
ny = 6

fname_one = "./camera_cal/calibration2.jpg"

images = glob.glob("./camera_cal/calibration*.jpg")

objpoints = []
imgpoints = []

objp = np.zeros((nx*ny, 3), np.float32)
objp[:,:2] = np.mgrid[0:nx,0:ny].T.reshape(-1,2)

for fname in images:
	print(fname)
	img = cv2.imread(fname)

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	ret,corners = cv2.findChessboardCorners(gray, (nx, ny), None)

	if ret == True:
		print("ret true")
		imgpoints.append(corners)
		objpoints.append(objp)

		cv2.drawChessboardCorners(img, (nx, ny), corners, ret)
		plt.imshow(img)
		plt.show()
		print("plot done")

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

img = cv2.imread(fname_one)

dst = cv2.undistort(img, mtx, dist, None, mtx)
implot = plt.imshow(dst)
plt.show()