"""
Pygame based simulation for approximating the value of pi using a monte-carlo
method.
"""

import random
import pygame
import math
from button import Button
from ten_tuple_queue import TenTuplesQueue
import sys
import pygame.freetype
from pygame.locals import *

pygame.init()


radius = 175
white = (255, 255, 255)
light_green = (0, 200, 0)
red = (255, 0, 0)
light_grey = (175, 175, 175)
black = (0, 0, 0)
precision = 10000
size = width, height = 900, 900
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
running = True
font = pygame.freetype.SysFont("Arial", 24)
screen.fill(light_grey)
number_back = pygame.Rect(45, 18, width - 25, 25)
display_box = pygame.Rect(0.05 * width, 0.2 * height, 0.5 * width, 0.8 * height)
pygame.draw.rect(screen, white, display_box)
square = pygame.Rect(display_box.centerx - 0.5 * radius,
                     display_box.centery - 0.25 * display_box.height - 0.5 * radius,
                     radius, radius)
square = pygame.draw.rect(screen, light_green, square)
circle = pygame.draw.circle(screen, light_green,
                            (display_box.centerx,
                             display_box.centery + 1/4 * display_box.height
                             ), radius)
in_circle = 0
in_square = 0

left_align_buttons = display_box.right + 30
one = Button(screen, left_align_buttons, display_box.top, 50, 50, value=1)
ten = Button(screen, left_align_buttons,
             one.get_rect().bottom + 20, 50, 50, value=10)
one_hundred = Button(screen, left_align_buttons, ten.get_rect().bottom + 20,
                     50, 50, value=100)
one_thousand = Button(screen, left_align_buttons,
                      one_hundred.get_rect().bottom + 20, 50, 50, value=1000)
buttons = [one, ten, one_hundred, one_thousand]
# button rendering is handled in their own constructors
last_ten_points = TenTuplesQueue()


def rand_point(left, right, top, bottom):
    while 1:
        yield random.randint(left, right), random.randint(top, bottom)


def check_circle(center, point):
    x1, y1 = center[0], center[1]
    x2, y2 = point[0], point[1]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2) <= radius


def check_square(square, point):
    return square.collidepoint(point)


def monte_carlo():
    global last_ten_points  # pylint: disable=global-statement
    global in_square
    global in_circle
    global square
    global circle
    global radius
    global one
    point = next(v)
    # calculate where the point is in the display box, not absolute coords
    point_in_scene = (point[0] - display_box.left, point[1] - display_box.top)
    last_ten_points.add(point_in_scene)
    points = str(last_ten_points).split("\n")
    y = one.get_rect().top
    pygame.draw.rect(screen, white, pygame.Rect(630, y, 150, 300))
    y += 15
    for p in points:
        ptext, prect = font.render(p, black)
        screen.blit(ptext, (650, y))
        y += font.size
    # print(point)
    # pygame.draw.circle(screen, red, point, 3)
    if check_square(square, point):
        in_square += 1
        pygame.draw.circle(screen, red, point, 3)
        # print(in_circle, in_square)
    elif check_circle(circle.center, point):
        in_circle += 1
        pygame.draw.circle(screen, red, point, 3)
        # print(in_circle, in_square)
    pygame.draw.rect(screen, light_grey, pygame.Rect(15, 50, 1000, 24))
    fraction, rect_frac = font.render(f"{in_circle} / {in_square}", black)
    screen.blit(fraction, (15, 50))
    try:
        return in_circle / in_square
    except ArithmeticError:  # in case in_square is zero
        return 0


def simulate(count):
    while count:
        pi_value = monte_carlo()
        pygame.draw.rect(screen, white, number_back)
        pie, rect = font.render(f"pi = {pi_value}", black)
        screen.blit(pie, (15, 20))
        pygame.display.flip()
        count -= 1


def full_reset():
    global last_ten_points
    global in_circle
    global in_square
    global one

    # reset values
    last_ten_points = TenTuplesQueue()
    in_circle = 0
    in_square = 0
    # update pi value
    pygame.draw.rect(screen, white, number_back)
    pie, rect = font.render("pi = 0.0", black)
    screen.blit(pie, (15, 20))
    # update fraction
    pygame.draw.rect(screen, light_grey, pygame.Rect(15, 50, 1000, 24))
    fraction, rect_frac = font.render(f"{in_circle} / {in_square}", black)
    screen.blit(fraction, (15, 50))
    # update points list
    pygame.draw.rect(screen, white, pygame.Rect(630, one.get_rect().top, 150, 300))
    # draw it all again
    reset_draw()


def reset_draw():
    global display_box
    global square

    pygame.draw.rect(screen, white, display_box)
    pygame.draw.rect(screen, light_green, square)
    pygame.draw.circle(screen, light_green,
                            (display_box.centerx,
                             display_box.centery + 1/4 * display_box.height
                             ), radius)
    pygame.display.flip()


i = 0
v = rand_point(display_box.left, display_box.right,
               display_box.top, display_box.bottom)

# otherwise nothing gets drawn until the simulation actually runs once
full_reset()
pygame.display.flip()
while running:
    clock.tick(60)
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    for button in buttons:
        if button.collidepoint(mouse_pos):
            button.on_hover()
        else:
            button.on_dehover()  # this adds extra unnecessary execution
    # might be odd to flip twice in one cycle, but we're ignoring the refresh
    # rate anyway when we draw for the actual simulation
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()

        # this could be better implemented with some listener or handler system
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # could be redundant, get it exact to be safe
            for button in buttons:
                if button.collidepoint(mouse_pos):
                    simulate(button.get_value())

        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[K_r]:
                if keys[K_LSHIFT] or keys[K_RSHIFT]:
                    full_reset()
                else:
                    reset_draw()
