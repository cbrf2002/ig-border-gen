from PIL import Image, ImageOps
import os

# Default border color and fixed border size.
DEFAULT_BORDER_COLOR = (255, 255, 255)  # White color
FIXED_BORDER = 50  # Fixed border width in pixels
ASPECT_RATIO = "4:5"  # Aspect ratio string (e.g. '4:5', '1:1', etc.)

def parse_aspect_ratio(aspect_ratio_str):
    """Convert a string aspect ratio (e.g. '4:5') to a decimal value."""
    width, height = map(int, aspect_ratio_str.split(":"))
    return height / width

def add_border(input_image_path, output_image_path, border_color, aspect_ratio):
    # Step 1: Add a fixed border to the original image.
    img = Image.open(input_image_path)
    iw, ih = img.size
    img_with_border = ImageOps.expand(img, border=FIXED_BORDER, fill=border_color)
    new_iw, new_ih = img_with_border.size

    # Step 2: Create a square (1:1) canvas.
    square_side = max(new_iw, new_ih)
    square_img = Image.new("RGB", (square_side, square_side), border_color)
    offset_x = (square_side - new_iw) // 2
    offset_y = (square_side - new_ih) // 2
    square_img.paste(img_with_border, (offset_x, offset_y))

    # Step 3: Expand the square into a canvas with the chosen aspect ratio.
    final_width = square_side
    final_height = int(round(aspect_ratio * square_side))  # Adjusting for dynamic aspect ratio

    final_img = Image.new("RGB", (final_width, final_height), border_color)
    offset_y_final = (final_height - square_side) // 2
    final_img.paste(square_img, (0, offset_y_final))

    # Step 4: Resize the image to 1080px width (for Instagram)
    base_width = 1080
    w_percent = base_width / float(final_img.size[0])
    h_size = int(float(final_img.size[1]) * float(w_percent))
    final_img = final_img.resize((base_width, h_size), Image.Resampling.LANCZOS)

    # Step 5: Ensure sRGB color profile and save as high-quality JPEG
    final_img = final_img.convert("RGB")  # Ensure it's in RGB mode
    final_img.save(output_image_path, format="JPEG", quality=95, optimize=True)

def main():
    # Automatically set input and output directories.
    parent_folder = os.path.dirname(os.path.abspath(__file__))

    # Assuming the input folder is named "Input" and output folder is "Done"
    input_path = os.path.join(parent_folder, "Input")
    output_path = os.path.join(parent_folder, "Done")
    border_color = DEFAULT_BORDER_COLOR

    # Convert aspect ratio string to decimal value
    aspect_ratio = parse_aspect_ratio(ASPECT_RATIO)

    # Check if the input directory exists.
    if not os.path.isdir(input_path):
        print(f"Input folder '{input_path}' does not exist.")
        return

    # Create the output directory if needed.
    if not os.path.isdir(output_path):
        os.makedirs(output_path, exist_ok=True)

    # Process images in the input directory.
    extensions = ('.png', '.jpg', '.jpeg')
    images_list = [f for f in os.listdir(input_path) if f.lower().endswith(extensions)]
    for image in images_list:
        in_img = os.path.join(input_path, image)
        base, ext = os.path.splitext(image)
        new_filename = f"{base}_BORDER{ext}"
        out_img = os.path.join(output_path, new_filename)
        add_border(in_img, out_img, border_color, aspect_ratio)

    print(f"Processed {len(images_list)} images.")

if __name__ == "__main__":
    main()
