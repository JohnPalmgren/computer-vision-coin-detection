import cv2
import class_solution

# Create original colour image.
original_image = cv2.imread('coin_picture.png', 1)
# Create greyscale image and add blur.
img = cv2.imread('coin_picture.png', cv2.IMREAD_GRAYSCALE)
img = cv2.GaussianBlur(img, (5,5), 0)

circle = class_solution.Circles(img)

poly = class_solution.Polygon(img)

values = class_solution.GetCoinValues(img)

circle.draw_circles(original_image)

poly.draw_polygons(original_image)

class_solution.add_results_to_image(
    values.circle_coin_values(circle.get_radius(),
    circle.get_brightness(20)), values.non_circle_values(poly.find_polygons()),
    poly.get_centre(), circle.find_circles(), original_image
    )

class_solution.show_image(original_image)
