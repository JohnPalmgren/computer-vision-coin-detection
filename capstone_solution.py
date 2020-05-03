import numpy as np
import cv2

#Create original colour image.
original_image = cv2.imread('coin_picture.png', 1)
# Create greyscale image.
img = cv2.imread('coin_picture.png', cv2.IMREAD_GRAYSCALE)
#Add blur.
img = cv2.GaussianBlur(img, (5,5), 0)

# Detect circles.
circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,0.9,120,param1=50,param2=27,minRadius=60,maxRadius=120)
# Create circle coordinates as integers
circles_int = np.uint16(np.around(circles))

count = 1
for i in (circles[0]):
    
    # Draw the outer circle. 
    cv2.circle(original_image, (i[0],i[1]), i[2], (255,0,0), 4)
    # Draw centre of circle.
    cv2.circle(original_image, (i[0],i[1]), 2, (0,0,255), 2)
    # Add text counting circles.
    #cv2.putText(original_image, str(count), (i[0],i[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0) ,2)
    count+=1

def get_radius(circles):
    radius = []
    for coords in circles[0,:]:
        radius.append (coords[2])
    return radius


def get_brightness(img, circles, size):
    """Mesure average number of pixle in a small sample area of the circle.
    
    img: image
    circles: interger values of co-ordinates of the circles in the image
    size: size of the sample area in which to take the avarage pixle value

    returns a list corresponding to the circles in the image, representing the brightness of each circle 
    """
    av_value = []
    for coords in circles[0,:]:
        #get average no of pixles (brightness)
        av_brightness = np.mean(img [coords[1] - size : coords[1] + size, coords[0] - size : coords[0] + size])
        #print (img[coords[1] - size : coords[1] + size, coords[0] - size : coords[0] + size])
        av_value.append(av_brightness)
    return av_value

radii = get_radius(circles_int)

bright_values = get_brightness(img,circles_int,20)

#print ('radii',radii,'\nbright value',bright_values)

def sort_coins(radii, bright_values):
    values = []
    
    for r,b in zip(radii,bright_values):
        if r > 110 and b > 170:
            values.append(10)
        elif r < 110 and b > 170:
            values.append(5)
        elif r > 110 and b < 170:
            values.append(2)
        elif r < 110 and b < 170:
            values.append(1)
    return values 

def add_results_to_image(coin_values,circles):
    # Add text to show total value of coins
    cv2.putText(original_image, f'Estimated total value {str(sum(coin_values))}p', (200,100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,0) ,2)
    # Add text to each coin with the coin value
    count=0
    for coords in circles[0,:]:
        cv2.putText(original_image, str(coin_values[count]), (coords[0],coords[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0) ,2)
        count+=1
    
coin_values = sort_coins(radii, bright_values)

add_results_to_image(coin_values,circles)


# Show image.
cv2.imshow('image', original_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
