import cv2
import numpy as np

class Circles():
    """Detect circles and properties of circles and draw them on image."""

    def  __init__(self, img):
        self.img = img

    def find_circles(self):
        """Use HoughCircles to detect circles in image. 
        Return co-ordinates of the circle and radius as numpy array. 
        """

        circles = cv2.HoughCircles(self.img, cv2.HOUGH_GRADIENT, 0.9, 120,
                                   param1=50, param2=27, minRadius=60,
                                   maxRadius=120)
        return np.uint16(np.around(circles))

    def get_radius(self):
        """Return a list of radius values"""

        return [coords[2] for coords in self.find_circles()[0,:]]

    def get_brightness(self, size):
        """Mesure average number of pixle in a sample area of the circle.
        size: size of the sample area to take the avarage pixle value
        returns a list corresponding to the circles in the image, 
        representing the brightness of each circle. 
        """

        av_value = []
        for coords in self.find_circles()[0,:]:
            # Get average no of pixles (brightness).
            av_brightness = np.mean(self.img [coords[1]-size : coords[1] 
                                    +size, coords[0]-size : coords[0] 
                                    +size])
            av_value.append(av_brightness)
        return av_value

    def draw_circles(self, image):
        """Draws circles onto an image.
        circles: numpy array containing co-ordinates and radius size.
        image: image on which to draw circles.
        """

        for i in self.find_circles()[0]:
            cv2.circle(image, (i[0], i[1]), i[2], (255 ,0, 0), 4)


class Polygon():
    """Detect polygon contour and crentre and draw contour."""

    def __init__(self, img):
        self.img = img

    def find_polygons(self):
        """Detect contours and area of shapes and filters by area."""

        imgcanny = cv2.Canny(self.img, 16, 14)
        kernel = np.ones((5, 5))
        imgdil = cv2.dilate(imgcanny, kernel, iterations=1)
        contours, hierarchy = cv2.findContours(imgdil, cv2.RETR_EXTERNAL, 
                                              cv2.CHAIN_APPROX_NONE)
    
        contour_list = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 60000 and area < 70000:
                contour_list.append(cnt)

        return contour_list
    
    def get_centre(self):
        """Returns co-ordinates for centre of polygons in image."""

        for cnt in self.find_polygons():
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
        return (x+w // 2, y+h // 2)

    def draw_polygons(self, image):
        """Draw contours around polygon in image."""

        for cnt in self.find_polygons():
            cv2.drawContours(image, cnt, -1, (255, 0, 0), 4)

           
class GetCoinValues():
    """Detect the value of each coin identified in the image."""

    def __init__(self, img):
        self.img = img

    def circle_coin_values(self, radii, brightness):
        """Return value of coins based on their brightness and radius"""

        values = []
        for r,b in zip(radii, brightness):
            if r > 110 and b > 170:
                values.append(10)
            elif r < 110 and b > 170:
                values.append(5)
            elif r > 110 and b < 170:
                values.append(2)
            elif r < 110 and b < 170:
                values.append(1)

        return values 

    def non_circle_values(self, polygons):
        """Return value of 50 for all non circle coins in image
        polygons: list of polygons in image
        """
        
        return [50 for coin in polygons]


def add_results_to_image(circle_coin_values, fifty_pence_values, 
                         polygon_centre, circles, image):
    """Display the total value and the value of each coin on the image
    
    circle_coin_values: list of values of coins excluding 50p
    fifty_pence_vlaues: list of 50p values
    polygon_centre: coordinates for centre of polygon
    circles: circle co-ordinates
    image: image on which to display results
    """

    # Add text to show total value of coins.
    cv2.putText(image, f"""Estimated total value {str(sum(circle_coin_values)
                        + sum(fifty_pence_values))}p""", (200, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0 ,0 ,0), 2)
    # Add text to each circle coin with the coin value.
    count = 0
    for coords in circles[0,:]:
        cv2.putText(image, str(circle_coin_values[count]), 
                    (coords[0], coords[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, 
                    (0, 0, 0), 2)
        count += 1
    # Add text to non-circle coins with coin value.
    cv2.putText(image, '50',  polygon_centre, cv2.FONT_HERSHEY_SIMPLEX, 2, 
               (0, 0, 0), 2)


def process_image(filename):
    """Convert to grey and add blur."""

    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    img = cv2.GaussianBlur(img, (5, 5), 0)

    return img
    

def show_image(image):
    """Display image."""

    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()