from PIL import Image, ImageDraw
import math


def draw_divided_circle(n, obj_coords, finger_coords, diagonal_len, threshold, background):
    # create a new image with black background
    size = 200
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # calculate circle properties
    cx, cy = size / 2, size / 2
    radius = size / 2 * 0.8

    # calculate the angle of each section
    section_angle = 2 * math.pi / n
    section_angle = np.rad2deg(section_angle)

    # calculate the angle between the finger and the object
    dx = obj_coords[0] - finger_coords[0]
    dy = obj_coords[1] - finger_coords[1]
    angle = math.atan2(dy, dx)
    angle = np.rad2deg(angle)
    print(angle)

    # calculate the distance between finger and object
    distance = math.sqrt(dx ** 2 + dy ** 2)

    # calculate the intensity of the color based on distance
    intensity = max(0, 1 - distance / diagonal_len)
    color = (int(255 * intensity), 0, 0, 255)

    for a in range(0, 360, int(section_angle)):
        draw.pieslice((0, 0, size, size), a, a + section_angle, fill=(0, 0, 0, 0))

    draw.pieslice((0, 0, size, size), 0, 360, fill=(0, 0, 0, 0), outline=color, width=10)

    starting_angle = angle // section_angle * section_angle
    draw.pieslice((0, 0, size, size), starting_angle, starting_angle + section_angle, fill=color, outline='black')

    if background is not None:
        bg_img = Image.open(background)
        bg_img.paste(img, (bg_img.width - size, 0), mask=img)
        return bg_img

    return img


draw_divided_circle(8, (500, 1000, 20), (500, 0, 0), 1500, 100, '/content/IMG_81381B39507A-1.jpeg')
