import cv2
import coin_solution

if __name__ == '__main__':

    filename = 'coin_picture.png'
    original_image = cv2.imread(filename, 1)
    img = coin_solution.process_image(filename)

    circle = coin_solution.Circles(img)

    poly = coin_solution.Polygon(img)

    values = coin_solution.GetCoinValues(img)

    circle.draw_circles(original_image)

    poly.draw_polygons(original_image)

    coin_solution.add_results_to_image(
        values.circle_coin_values(circle.get_radius(),
        circle.get_brightness(20)), values.non_circle_values
        (poly.find_polygons()), poly.get_centre(), circle.find_circles(), 
        original_image
        )

    coin_solution.show_image(original_image)
