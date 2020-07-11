import cv2
import coins_solution

# image_test = cv2.imread('image_test.png', cv2.IMREAD_GRAYSCALE)
# img = cv2.GaussianBlur(image_test, (5,5), 0)

def test_find_circles():

    
     circles = coins_solution.find_circles(data)

#      assert circles == np.uint16(np.around([[[1354  250  119]
#   [1630  282   90]
#   [ 974  638  102]
#   [1206  744  107]
#   [ 994  132  108]
#   [1692  506  119]
#   [1260  466  107]
#   [1522  340  113]
#   [1364  394  118]
#   [1232  344  113]
#   [1418  612  110]
#   [1548  462  108]
#   [1480  214  108]
#   [1690  386   75]
#   [ 908  320  100]
#   [1084  480   93]]]))

     #assert len(circles[0,:]) == 8 # Number of circles in image 
     #return len(circles[0,:])
     
     c = []

     c.append(circ for circ in circles())

     return c

print (test_find_circles())

#coins_solution.show_image(image_test)