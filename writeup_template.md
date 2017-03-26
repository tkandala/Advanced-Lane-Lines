##Writeup Template
###You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./output_images/undistorted_warped_chessboard.png "Undistorted"
[image2]: ./test_images/test1.jpg "Test Image 1"
[image3]: ./output_images/undistorted_compare_test1.png "Road undistorted"
[image4]: ./output_images/sobel_colorChannel_test1.png "Road Transformed"
[image5]: ./output_images/binary_warped_compare.png "Warp Example"
[image6]: ./output_images/lane_lines.png "Fit Visual"
[image7]: ./output_images/lanes_lines_margin_window.png "Fit Visual with margin window"
[image8]: ./output_images/lane_lines_unwarped.png "Output"
[image9]: ./output_images/sobel_output.png "Output"
[video1]: ./project_video.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points
###Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
###Writeup / README

####1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  [Here](https://github.com/udacity/CarND-Advanced-Lane-Lines/blob/master/writeup_template.md) is a template writeup for this project you can use as a guide and a starting point.  

You're reading it!

###Camera Calibration

####1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the first 2 code cells of the IPython notebook located in "./advanced-lane-finding.ipynb"

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 

![alt text][image1]

###Pipeline (single images)

####1. Provide an example of a distortion-corrected image.

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one:

![alt text][image2]

You can find the results of undistort and comparison here:

![alt text][image3]

####2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

I used a combination of color and gradient thresholds to generate a binary image.  Here's an example of my output for this step. 

![alt text][image4]

Basically, I have used x & y gradients along with gradient magnitude and gradient direction to arrive at my first set of identifying lane lines using just the gradient. An example of this sobel output step can be seen below:

![alt text][image9]

The choice of Kernal Size I have settled with is 3, a threshold size from 20 to 100 and gradient magnitude threshold (100,150). I have used the threshold of (0, np.pi/2) for the gradient direction - same as the one in lecture notes.

After the sobel filter, I have used the s color channel to further identify the lane lines. For this, I have used the threshold (90, 255). The low number of 90 allowed me to properly retain the lane lines, especially during the points where there are tree shadows on the highway. 

####3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `getWarped()`, which appears in the code cell below the "Perspective Transform" heading of the IPython notebook.  The `getWarped()` function takes as inputs an image (`img`), as well the binary image.  I chose the hardcode the source and destination points inside the '`getWarped()` in the following manner:

```
src = np.float32(
    [[-330, image.shape[0]], 
    [475, 470], 
    [800, 470], 
    [1570, image.shape[0]]])
dst = np.float32(
    [[0, image.shape[0]], 
    [0, 0], 
    [image.shape[1], 0], 
    [image.shape[1], image.shape[0]]])

```
This resulted in the following source and destination points:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| -330, 720     | 0, 720        | 
| 475, 470      | 0, 0          |
| 800, 470      | 1280, 0       |
| 1570, 720     | 1280, 720     |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![alt text][image5]

####4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

I have used the same sliding window method as in the lecture notes to find my lane lines. I felt this was a straight forward to approach the problem. The code can be found in the cell below the "Extract Lane Lines" title in the IPython notebook. I have used 3 functions: `getNonZeroPixels()`, `generateFreshLanePoints()` and `extract_lines()` to get the lanes lines. 

`getNonZeroPixels()` is just a helper function to get the non-zero pixels from the binary unwarped image. `generateFreshLanePoints()` uses the histogram method along with the sliding window method to extract the lane lines. I have used a default of 9 windows, a margin of 100px and min pixels of 50 to identify the lane points from the binary image.

`extract_lines()` takes in the indexes of all the left and right lane points to fit a polynomial through these points. What we get are the coefficients of 2nd degree polynomial that will help us get the x coordinate of the lane for any y value. We know that there could be more than one y value for a x point because of the lanes being vertical so it is better to get a polynomial that is a function of y instead of x. 

The final lanes can be seen here:

![alt text][image6]

The search window of 100 pixels margin that we have seen earlier can be seen the image below with the windows in green. This will also help us identify the lane points in the next frame of the video without actually performing the `generateFreshLanePoints()` again. This is done inside the `generateLanePointsFromPrevious()` function in the cell below the "Extract Lanes from Previous Lanes" title.

![alt text][image7]

####5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I did this in the cell below the "Radius of Curvature and Vehicle Position" heading of the IPython Notebook. I have used the code snippets from the lecture notes to calculate the Radius of Curvature. Similar to Lecture notes, the radius of curvature is calculated at the max y position which will be the bottom of the image. Based on the the un-warped (bird's eye view) lane lines, the width of the lane lines in pixel space came up to 600px. 

For the distance from center, I have calculated the x positions of both the left and right lanes at max y - which will be at the bottom of the image. With these x positions, I was able to get the lane center and then taking the x = 1280/2 = 640px as the vehicle center, I was able to check how many pixels the vehicle center was from the lane center. Multiplying that with the pixel to meter factor, we get the correct position of the vehicle from the center.

####6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step after the `drawLane()` function which is after the "Draw Lane" heading of the IPython notebook.  Here is an example of my result on a test image:

![alt text][image8]

The drawLane() function takes in the image, binary warped image, the perspective transform matrix, along with the x & y points of the lane to create the polygon that will be our basis to create the lane projection. After the polygon is generated, it is transformed back to the original image space using inverse perspective Matrix and added to the original image.

---

###Pipeline (video)

####1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video.mp4)

---

###Discussion

####1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.

So I have used the techniques discussed in lecture notes and basically utilized the sample code from the notes to build up my pipeline to identify the lane lines. This was probably the easy step in getting to the solution quickly. With some tuning to the paramters, especially in the sobel and color channels, I was able to extract the lane lines pretty decently all throughout the video.

As we can see, there are some wobly lane lines in the right lane when passing beside the tree shadows or when the road's surface switched from tar to concrete. We can tackle these issues in couple of ways.

First, as we do during driving, or at least how I drive is that if the lane lines are not properly visible on one side, I will usually follow the other side of the lane line and try to stick to it so I don't go off lane. We can definetely do something like that here too. Since the left lane line is pretty solid throughout the whole video, we can just rely on it's line ploynomial to replicate the right lane line - based on the 600px width difference between the 2 lanes. This will remove the wobly effect we see from the frames.

The other method which can be complicated is to have dynamic parameters that get tuned automatically based on the surroundings like when approaching shadow area. This is easy said than done because we will have to constantly monitor our surroundings and determine what our parameters are going to be. We can take a pre-defined set of parameters based on various conditions and use them to extract the lane lines. Probably this is more beneficial when driving during night times or when we cannnot rely completely on one sided lane to extract other lane.

