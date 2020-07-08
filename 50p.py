import cv2
import numpy as np
import capstone_solution as cs

#Create original colour image.
original_image = cv2.imread('coin_picture.png', 1)
# Create greyscale image and add blur.
img = cv2.imread('coin_picture.png', cv2.IMREAD_GRAYSCALE)
img = cv2.GaussianBlur(img, (5,5), 0)


fifty_contours = cs.find_50p(img)[0] # Contours of 50p coins

fifty_coins_value = cs.find_50p(img)[1]*50 # Value of of 50p coins in image. 

cs.draw_50p(fifty_contours, original_image)


cs.show_image(original_image)