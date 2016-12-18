__author__ = 'BrianUser'

import pygame
import math
import random

pygame.init()

display_width = 800
display_height = 600
caption = 'Asteroids'
pygame.display.set_caption(caption, 'Asteroids')

black = (0, 0, 0)
white = (255, 255, 255)

gameDisplay = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
crashed = False
playing = False

font = pygame.font.SysFont("Times New Roman, Arial", 30)


def render(x, y, sprite):
    gameDisplay.blit(sprite, (x, y))


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


class ship:
    x = 400
    y = 300
    angle = 0
    renderangle = 0
    acceleration = 0
    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.image.load("ship.png")


class asteroid:
    x = random.randint(0, 800)
    y = random.randint(0, 600)
    angle = 0
    renderangle = 0
    sprite = pygame.sprite.Sprite()


class game:
    title = "Asteroids"
    text = "Start"
    bgcolor = black


bullets = []
bullet = pygame.sprite.Sprite()
bullet.image = pygame.image.load("bullet.png")

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            Mouse_x, Mouse_y = pygame.mouse.get_pos()
            bullets.append([ship.x, ship.y, math.atan2((-Mouse_x+ship.x),(-Mouse_y+ship.y))])
    if pygame.key.get_pressed()[pygame.K_w] != 0:
        ship.acceleration = 6
    if pygame.key.get_pressed()[pygame.K_a] != 0:
        ship.angle += .1
        ship.renderangle += 5.72957795
    if pygame.key.get_pressed()[pygame.K_d] != 0:
        ship.angle -= .1
        ship.renderangle -= 5.72957795
    if ship.x >= 800:
        ship.x = 5
    if ship.x <= 0:
        ship.x = 795
    if ship.y >= 600:
        ship.y = 5
    if ship.y <= 0:
        ship.y = 595
    angle = font.render("{0}".format(ship.angle), True, white)
    ship.x -= math.sin(ship.angle) * ship.acceleration
    ship.y -= math.cos(ship.angle) * ship.acceleration
    if ship.acceleration >= 2:
        ship.acceleration *= 0.95
    render(ship.x-18, ship.y-18, rot_center(ship.sprite.image, ship.renderangle))
    for b in bullets:
        render(b[0], b[1], bullet.image)
    for b in range(len(bullets)):
        bullets[b][0] -= math.sin(bullets[b][2]) * 14
        bullets[b][1] -= math.cos(bullets[b][2]) * 14
    for b in bullets:
        if b[0] < 0 or b[0] > 800 or b[1] < 0 or b[1] > 600:
            bullets.remove(b)
    render(10, 0, angle)
    pygame.display.update()
    clock.tick(50)
    gameDisplay.fill(game.bgcolor)
pygame.quit()
quit()
