import cv2
import capstone_solution as cs

if __name__ == '__main__':

    #Create original colour image.
    original_image = cv2.imread('coin_picture.png', 1)
    # Create greyscale image and add blur.
    img = cv2.imread('coin_picture.png', cv2.IMREAD_GRAYSCALE)
    img = cv2.GaussianBlur(img, (5,5), 0)

    circles = cs.find_circles(img)

    radii = cs.get_radius(circles)

    bright_values = cs.get_brightness(img,circles,20)

    fifty_contours = cs.find_50p(img)[0] # Contours of 50p coins

    fifty_coins_value = cs.find_50p(img)[1]*50 # Value of of 50p coins in image. 

    coin_values = cs.sort_coins(radii, bright_values)

    cs.draw_circles(circles, original_image)

    cs.draw_50p(fifty_contours, original_image)

    cs.add_results_to_image(coin_values, fifty_coins_value, circles, original_image)

    cs.show_image(original_image)
