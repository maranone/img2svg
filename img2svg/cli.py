import argparse
from img2svg.image_processing import download_and_resize_image
from img2svg.svg_conversion import image_to_svg
import os

default_image_link = "https://t4.ftcdn.net/jpg/09/77/54/79/240_F_977547957_KCF6SHZaZqx6FyUACiQbjNtuy6bZafx3.webp"

# Define presets with increments for hue, saturation, and value
PRESETS = {
    'slow': {'hue_increment': 20, 'saturation_increment': 20, 'value_increment': 20, 'min_contour': 0.01, 'smooth_epsilon': 0.00001, 'resize_original': 1},
    'fast': {'hue_increment': 90, 'saturation_increment': 90, 'value_increment': 90, 'min_contour': 0.06, 'smooth_epsilon': 0.00050, 'resize_original': 8}
}

def main():
    parser = argparse.ArgumentParser(description='Image Processing and SVG Conversion Tool')
    parser.add_argument('--image', type=str, default=default_image_link, help='URL or Path of the image')
    parser.add_argument('--output_dir', type=str, default='.', help='Output directory for files')
    parser.add_argument('--hue_increment', type=int, default=45, help='Hue increment value')
    parser.add_argument('--saturation_increment', type=int, default=45, help='Saturation increment value')
    parser.add_argument('--value_increment', type=int, default=45, help='Value increment value')
    parser.add_argument('--min_contour', type=float, default=0.01, help='Threshold for smoothing (epsilon value)')
    parser.add_argument('--smooth_epsilon', type=float, default=0.00001, help='Value for smoothing vectors')
    parser.add_argument('--resize_original', type=float, default=2, help='Faster processing dividing width/height by this number')
    parser.add_argument('--preset', type=str, choices=PRESETS.keys(), help='Preset to use for color increments')

    args = parser.parse_args()

    # Apply preset values if a preset is selected
    if args.preset:
        preset_values = PRESETS[args.preset]
        # Update args with the preset values, but allow command-line args to override them
        for key, value in preset_values.items():
            if getattr(args, key) == parser.get_default(key):
                setattr(args, key, value)

    if args.resize_original == 0:
        args.resize_original = 1
    image_path, new_width, new_height = download_and_resize_image(args.image, args.resize_original)
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    svg_path = f"{args.output_dir}/{base_name}_regions.svg"
    print(f"Image saved at: {image_path}")
    image_to_svg(image_path, svg_path, new_width, new_height, 
             args.hue_increment, args.saturation_increment, 
             args.value_increment, args.min_contour, args.smooth_epsilon)
    print(f"SVG path: {svg_path}")    

if __name__ == '__main__':
    main()
