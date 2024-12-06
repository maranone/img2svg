import cv2
import numpy as np
import svgwrite

def image_to_svg(image_path, svg_path, new_width, new_height, hue_increment=45, saturation_increment=45, value_increment=45, min_contour=0.01, smooth_epsilon=0.00001):
    original_image = cv2.imread(image_path)
    hsv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
    color_ranges = []

    for h in range(0, 180, hue_increment):
        for s in range(0, 256, saturation_increment):
            for v in range(0, 256, value_increment):
                lower_bound = np.array([h, s, v])
                upper_bound = np.array([h + hue_increment, s + saturation_increment, v + value_increment])
                color_ranges.append((lower_bound, upper_bound))

    dwg = svgwrite.Drawing(svg_path, profile='tiny', size=(new_width, new_height))
    dwg.viewbox(0, 0, new_width, new_height)

    for lower_bound, upper_bound in color_ranges:
        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        combined_path = svgwrite.container.Group()

        for contour in contours:
            if len(contour) >= min_contour:
                epsilon = smooth_epsilon * cv2.arcLength(contour, True)
                simplified_contour = cv2.approxPolyDP(contour, epsilon, True)
                color_sample = original_image[simplified_contour[0][0][1], simplified_contour[0][0][0]]
                path_data = 'M ' + ' '.join([f'{x},{y}' for [x, y] in simplified_contour[:, 0]]) + ' Z'
                path = svgwrite.path.Path(d=path_data, fill=f'rgb({color_sample[2]},{color_sample[1]},{color_sample[0]})')
                combined_path.add(path)

        dwg.add(combined_path)
    dwg.save()
