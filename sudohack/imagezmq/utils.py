
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint


def read_img(file_name):
	img = cv2.imread(file_name)
	return img

def resize_img(image, scale):
	res = cv2.resize(image, None, fx=scale, fy=scale, interpolation = cv2.INTER_AREA)
	return res


def img_to_gray(image):
	img_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	return img_gray


def img_to_gaussian_gray(image):
	img_gray = cv2.GaussianBlur(img_to_gray(image), (5, 5), 0)
	return img_gray


def img_to_neg(image):
	img_neg = 255 - image
	return img_neg


def binary_thresh(image, threshold):
	retval, img_thresh = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
	return img_thresh


def adaptive_thresh(image):
	img_thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 8)
	return img_thresh


def sobel_edge(image, align):
	img_horiz = cv2.Sobel(image, cv2.CV_8U, 0, 1)
	img_vert = cv2.Sobel(image, cv2.CV_8U, 1, 0)
	if align == 'h':
		return img_horiz
	elif align == 'v':
		return img_vert
	else:
		print('use h or v')


def sobel_edge2(image):
	grad_x = cv2.Sobel(image, cv2.CV_16S, 1, 0, ksize=3, borderType = cv2.BORDER_DEFAULT)
	grad_y = cv2.Sobel(image, cv2.CV_16S, 0, 1, ksize=3, borderType = cv2.BORDER_DEFAULT)

	abs_grad_x = cv2.convertScaleAbs(grad_x)
	abs_grad_y = cv2.convertScaleAbs(grad_y)

	dst = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
	return dst


# canny edge operator
def canny_edge(image, block_size, ksize):
	img = cv2.Canny(image, block_size, ksize)
	return img


# laplacian edge
def laplacian_edge(image):
	# good for text
	img = cv2.Laplacian(image, cv2.CV_8U)
	return img


# detect countours
def find_contours(image):
	(_, contours, _) = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	contours = sorted(contours, key = cv2.contourArea, reverse = True)[:5]
	return contours


def median_blur(image):
	blurred_img = cv2.medianBlur(image, 3)
	return blurred_img


def dilate_img(image):
	img = cv2.dilate(image, np.ones((5,5), np.uint8))
	return img


def close(image):
	img = cv2.Canny(image, 75, 300)
	img = cv2.dilate(img, None)
	img = cv2.erode(img, None)
	return img


def harris_edge(image):
	img_gray = np.float32(image)

	corners = cv2.goodFeaturesToTrack(img_gray, 4, 0.03, 200, None, None, 2,useHarrisDetector=True, k=0.04)
	corners = np.int0(corners)

	for corner in corners:
		x, y = corner.ravel()
		cv2.circle(image, (x, y), 3, 255, -1)
	return image


def histogram(image):
	hist = cv2.calcHist([image], [0], None, [256], [0, 256])
	plt.plot(hist)
	plt.show()


# fast fourier transform
def fourier(image):
	f = np.fft.fft2(image)
	fshift = np.fft.fftshift(f)
	magnitude_spectrum = 20 * np.log(np.abs(fshift))

	plt.subplot(121), plt.imshow(image, cmap='gray')
	plt.title('Input Image'), plt.xticks([]), plt.yticks([])

	plt.subplot(122), plt.imshow(magnitude_spectrum, cmap='gray')
	plt.title('FFT'), plt.xticks([]), plt.yticks([])

	plt.show()


# calculate scale and fit into display
def display(window_name, image):
	screen_res = 1440, 900	# MacBook Air
	
	scale_width = screen_res[0] / image.shape[1]
	scale_height = screen_res[1] / image.shape[0]
	scale = min(scale_width, scale_height)
	window_width = int(image.shape[1] * scale)
	window_height = int(image.shape[0] * scale)

	cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
	cv2.resizeWindow(window_name, window_width, window_height)

	cv2.imshow(window_name, image)

	cv2.waitKey(0)
	cv2.destroyAllWindows()