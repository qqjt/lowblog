from PIL import Image
import os.path


def resize_img_to_half(img_path):
    img = Image.open(img_path)
    width, height = img.size
    f_name, f_ext = os.path.splitext(img_path)
    while width > 2000 and width % 2 == 0 and height % 2 == 0:
        print('resizing:', img_path, width, height)
        width = width >> 1
        height = height >> 1
        new_img = img.resize((width, height))
        new_path = f'{f_name}-small{f_ext}'
        new_img.save(new_path)
    else:
        print('ignore:', img_path, width, height)


def is_image_file(file_path):
    # List of common image file extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'}

    # Get the file extension
    _, file_extension = os.path.splitext(file_path)

    # Check if the file extension is in the list of image extensions
    return file_extension.lower() in image_extensions


def resize_dir(source_dir):
    for f in os.listdir(source_dir):
        f_path = os.path.join(source_dir, f)
        if is_image_file(f_path):
            resize_img_to_half(f_path)


if __name__ == '__main__':
    import sys

    _, s_dir = sys.argv
    resize_dir(s_dir)
