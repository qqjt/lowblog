from PIL import Image
import os.path


def resize_img_to_half(img_path):
    img = Image.open(img_path)
    width, height = img.size
    f_name, f_ext = os.path.splitext(img_path)
    result_path = img_path
    while width > 2000 and width % 2 == 0 and height % 2 == 0:
        print('resizing:', img_path, width, height)
        width = width >> 1
        height = height >> 1
        new_img = img.resize((width, height))
        new_path = f'{f_name}-small{f_ext}'
        new_img.save(new_path)
        result_path = new_path
    else:
        print('ignore:', img_path, width, height)
    return result_path


def is_image_file(file_path):
    # List of common image file extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'}

    # Get the file extension
    _, file_extension = os.path.splitext(file_path)

    # Check if the file extension is in the list of image extensions
    return file_extension.lower() in image_extensions


def replace_md_image_src(post_md_lines, old_f_name, new_f_name):
    result_lines = []
    search_string = f'({old_f_name})'
    replace_string = f'({new_f_name})'
    for l in post_md_lines:
        l = l.replace(search_string, replace_string)
        result_lines.append(l)
    return result_lines


def resize_dir(source_dir):
    # read md file lines
    post_md_file = source_dir.rstrip('\\/')
    post_md_file = post_md_file + '.md'
    post_md_lines = []
    with open(post_md_file, 'r', encoding='utf-8') as f:
        for l in f:
            post_md_lines.append(l)
    for f in os.listdir(source_dir):
        f_path = os.path.join(source_dir, f)
        if is_image_file(f_path):
            result_path = resize_img_to_half(f_path)
            if result_path != f_path:
                old_f_name = os.path.basename(f_path)
                new_f_name = os.path.basename(result_path)
                post_md_lines = replace_md_image_src(post_md_lines, old_f_name, new_f_name)
    # write back md lines
    with open(post_md_file, 'w', encoding='utf-8') as f:
        for l in post_md_lines:
            f.write(l)


if __name__ == '__main__':
    import sys

    _, s_dir = sys.argv
    resize_dir(s_dir)
