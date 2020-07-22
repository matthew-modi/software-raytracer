#!/usr/bin/env python
"""Python raytracer built from scratch by Matthew Modi, 2020"""

import random
import time

import matplotlib.pyplot as plt
import multiprocessing
from multiprocessing import Pool
import PIL as pil
import png
import numpy as np

from box import Box
from image import Image
from color import Color
from plane import Plane
from ray import Ray
import math

from sphere import Sphere
from vector2f import Vector2f
from vector3f import Vector3f


def main():
    # User selected constants:
    WIDTH = 800
    HEIGHT = 800
    FOV = 90

    CAMERA_POS = Vector3f(0.0, 0.0, 0.0)
    CAMERA_X = Vector3f(1.0, 0.0, 0.0).normalize()
    CAMERA_Y = Vector3f(0.0, 1.0, 0.0).normalize()
    CAMERA_Z = Vector3f(0.0, 0.0, 1.0).normalize()

    # objects = []
    # num_spheres = 7
    # for i in range(num_spheres):
    #     pos = Vector3f(random.uniform(-3, 3), random.uniform(-3, 3), random.uniform(-5, -10))
    #     radius = random.uniform(0.5, 1)
    #     color = Color(random.uniform(0, 1), 0.5, 1.0, type='hsv')
    #     objects.append(Sphere(pos, radius, color))

    objects = [Sphere(Vector3f(0.0, 0.0, -6.0), 1.8, Color(random.uniform(0, 1), 0.5, 1.0, type='hsv')),
               Plane(Vector3f(0.0, -2.0, 0.0), Vector3f(0.0, 1.0, 0.0))]

    print('Rendering...')
    render_start_time = time.time()
    img = render(WIDTH, HEIGHT, FOV, CAMERA_POS, {'x': CAMERA_X, 'y': CAMERA_Y, 'z': CAMERA_Z}, objects)
    print('Render Complete: ' + str(time.time()-render_start_time) + 's')

    print('Saving...')
    pixels = img.get_pixels()
    pixels_final = []
    for row in pixels:
        row_final = []
        for pixel in row:
            for color in pixel:
                row_final.append(int(color * 255))
        pixels_final.append(row_final)
    file_name = time.strftime('output/%y-%m-%d-%H-%M-%S') + '.png'
    file = open(file_name, 'wb')
    png.Writer(WIDTH, HEIGHT, greyscale=False).write(file, pixels_final)
    file.close()

    print('Displaying...')
    # plt.imshow(img.get_pixels())
    # plt.show()

    pil.Image.open(file_name).show()


def render(WIDTH, HEIGHT, fov_degrees, CAMERA_POS, camera_axes, objects) -> Image:
    # Generated constants:
    ASPECT_RATIO = WIDTH / HEIGHT
    if ASPECT_RATIO >= 1:
        WIDTH_DOMINANT = 1
    else:
        WIDTH_DOMINANT = 0
    ASPECT_RATIO = Vector2f((ASPECT_RATIO ** WIDTH_DOMINANT), (ASPECT_RATIO ** (1 - WIDTH_DOMINANT)))

    FOV = fov_degrees * math.pi / 180

    CAMERA_X = camera_axes['x']
    CAMERA_Y = camera_axes['y']
    CAMERA_Z = camera_axes['z']

    CAMERA_ORIENTATION_MATRIX = np.array([[0.0], [0.0], [0.0]])
    CAMERA_ORIENTATION_MATRIX = np.concatenate((CAMERA_ORIENTATION_MATRIX, np.rot90(np.array([CAMERA_X.raw()]), 3)),
                                               axis=1)
    CAMERA_ORIENTATION_MATRIX = np.concatenate((CAMERA_ORIENTATION_MATRIX, np.rot90(np.array([CAMERA_Y.raw()]), 3)),
                                               axis=1)
    CAMERA_ORIENTATION_MATRIX = np.concatenate((CAMERA_ORIENTATION_MATRIX, np.rot90(np.array([CAMERA_Z.raw()]), 3)),
                                               axis=1)
    CAMERA_ORIENTATION_MATRIX = np.delete(CAMERA_ORIENTATION_MATRIX, 0, 1)

    CAMERA_TO_WORLD_MATRIX = CAMERA_ORIENTATION_MATRIX
    CAMERA_TO_WORLD_MATRIX = np.concatenate((CAMERA_TO_WORLD_MATRIX, np.rot90(np.array([[0.0, 0.0, 0.0]]), 3)), axis=1)
    CAMERA_TO_WORLD_MATRIX = np.concatenate((CAMERA_TO_WORLD_MATRIX, np.array([CAMERA_POS.raw() + [1.0]])), axis=0)

    img = Image(WIDTH, HEIGHT)

    pixel_set = [(WIDTH, HEIGHT, FOV, CAMERA_POS, CAMERA_ORIENTATION_MATRIX, ASPECT_RATIO, objects, x, y)for y in range(HEIGHT) for x in range(WIDTH) ]

    data_set = []
    with Pool(processes=multiprocessing.cpu_count()) as pool:
        data_set = pool.starmap(render_pixel, pixel_set)

    i = 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            img.set_pixel(x, y, data_set[i])
            i += 1
    return img

def render_pixel(WIDTH, HEIGHT, FOV, CAMERA_POS, CAMERA_ORIENTATION_MATRIX, ASPECT_RATIO, objects, x, y):
    pixel_x = (2 * ((x + 0.5) / WIDTH) - 1) * math.tan(FOV / 2) * ASPECT_RATIO.x
    pixel_y = (1 - 2 * ((y + 0.5) / HEIGHT)) * math.tan(FOV / 2) * ASPECT_RATIO.y
    pixel_pos = (CAMERA_ORIENTATION_MATRIX.dot(np.array([[pixel_x], [pixel_y], [-1]])))
    ray_direction = Vector3f(pixel_pos[0][0], pixel_pos[1][0], pixel_pos[2][0]).normalize()
    primary_ray = Ray(CAMERA_POS, ray_direction)

    color = cast_ray(primary_ray, objects).raw()
    return color

def cast_ray(ray: Ray, objects: list) -> Color:
    hit_color = Color()
    trace_result = trace(ray, objects)
    t, i = trace_result['t'], trace_result['i']
    if t < float('inf'):
        hit_pos = ray.origin + ray.direction * t
        surface_data = objects[i].get_surface_data(hit_pos)
        hit_normal, hit_texture = surface_data['normal'], surface_data['texture']
        object_color = objects[i].color

        scale = 4
        x_state = round(hit_texture.x * scale % 1)
        pattern = int((x_state / 2) ** (round((hit_texture.y * scale + x_state * 0.5) % 1))) / 2 + 0.5
        hit_color = object_color * pattern * abs(hit_normal.dot(-ray.direction))
    return hit_color


def trace(ray: Ray, objects: list) -> dict:
    t_nearest = float('inf')
    hit_object_index = -1
    i = -1
    for shape in objects:
        i += 1
        t = shape.intersect(ray)
        if 0 < t < t_nearest:
            t_nearest = t
            hit_object_index = i

    return {'t': t_nearest, 'i': hit_object_index}


if __name__ == "__main__":
    main()
