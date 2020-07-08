import numpy as np
import cv2
  
def find_circles(img):
    """Use HoughCircles to detect circles in image. 

    return co-ordinates of the circle on the image and the size of the radius as an integer value 
    """

    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,0.9,120,param1=50,param2=27,minRadius=60,maxRadius=120)
    return np.uint16(np.around(circles))

def draw_circles(circles,image):
    """Draws circles onto an image.

    circles: list containing xy co-ordinates and the size of radius.
    image: image on which to draw circles.
    """
    count = 1
    for i in (circles[0]):
    
        # Draw the outer circle. 
        cv2.circle(image, (i[0],i[1]), i[2], (255,0,0), 4)

        count+=1

def find_50p(img):
    """Detect contours and area of shapes in the image and filters to detect 50p.

    Return contours matching the area of 50p and number of 50 pence detected.
    """

    imgcanny = cv2.Canny(img,16,14)
    kernel = np.ones((5, 5))
    imgdil = cv2.dilate(imgcanny, kernel, iterations=1)

    contours, hierarchy = cv2.findContours(imgdil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    fifty = []
    count = 0
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 60000 and area < 70000:
            fifty.append(cnt)
            count += 1


    return fifty, count


def draw_50p(contours, image):
    """Draw contours around 50p in image
    
    contours: co-ordinates for contours around detected 50 pence
    image: image on which to draw contours
    """

    for cnt in contours:
        cv2.drawContours(image, cnt, -1, (255, 0, 0), 4)
        cv2.putText(image, "50",  (835,393), cv2.FONT_HERSHEY_SIMPLEX, 2, #get position from coords
                    (0, 0, 0), 2)


def get_radius(circles):
    """Return a list of radius values

    Circles: a list of co-ordinates and radius of circles in image.
    """

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
        av_value.append(av_brightness)
    return av_value

def sort_coins(radii, bright_values):
    """Return value of coins based on their brightness and radius"""

    values = []
    
    for r,b in zip(radii, bright_values):
        if r > 110 and b > 170:
            values.append(10)
        elif r < 110 and b > 170:
            values.append(5)
        elif r > 110 and b < 170:
            values.append(2)
        elif r < 110 and b < 170:
            values.append(1)


    return values 

def add_results_to_image(circle_coin_values, fifty_pence_values, circles, image):
    """Display the total value and the value of each coin on the image
    
    circle_coin_values: list of values of coins excluding 50p
    fifty_pence_vlaues: values of 50 pence
    circles: circle co-ordinates
    image: image on which to display results
    """

    # Add text to show total value of coins
    cv2.putText(image, f'Estimated total value {str(sum(circle_coin_values)+fifty_pence_values)}p', (200,100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,0) ,2)
    # Add text to each coin with the coin value
    count=0
    for coords in circles[0,:]:
        cv2.putText(image, str(circle_coin_values[count]), (coords[0],coords[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0) ,2)
        count+=1
    
def show_image(image):
    """Display image"""

    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
