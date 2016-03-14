

# import freenect
# import cv2
# import numpy as np
 
# """
# Grabs a depth map from the Kinect sensor and creates an image from it.
# """
# def getDepthMap():    
#     depth, timestamp = freenect.sync_get_depth()
 
#     np.clip(depth, 0, 2**10 - 1, depth)
#     depth >>= 2
#     depth = depth.astype(np.uint8)
 
#     return depth
 
# while True:
#     depth = getDepthMap()
 
#     blur = cv2.GaussianBlur(depth, (5, 5), 0)
 
#     cv2.imshow('image', blur)
#     cv2.waitKey(10)





#!/usr/bin/python

# Standard imports
import cv2
import numpy as np;

# Read image
im = cv2.imread("james.jpg")

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 10
params.maxThreshold = 200


# Filter by Area.
params.filterByArea = True
params.minArea = 1500

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.1

# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.87

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01

# Create a detector with the parameters
detector = cv2.SimpleBlobDetector(params)


# Detect blobs.
keypoints = detector.detect(im)

a = None
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
# the size of the circle corresponds to the size of blob

im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show blobs
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)