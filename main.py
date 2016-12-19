__author__ = 'BrianUser'

import pygame
import math
import random
import time

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

font = pygame.font.Font("resources/vgaoem.fon", 15)


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


class game:
    score = 0
    bgcolor = black
    title = "Asteroids"
    text = "Press Space To Start"
    gameover = "Game Over! Your score was:"


bullets = []
bullet = pygame.sprite.Sprite()
bullet.image = pygame.image.load("bullet.png")

asteroids = []
asteroid = pygame.sprite.Sprite()
asteroid.image = pygame.image.load("asteroid.png")

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                playing = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if playing == True:
                Mouse_x, Mouse_y = pygame.mouse.get_pos()
                bullets.append([ship.x + 15, ship.y + 17, math.atan2((-Mouse_x + ship.x), (-Mouse_y + ship.y)), False])
    if playing == True:
        if pygame.key.get_pressed()[pygame.K_w] != 0:
            ship.acceleration = 6
        if pygame.key.get_pressed()[pygame.K_a] != 0:
            ship.angle += .1
            ship.renderangle += 5.72957795
        if pygame.key.get_pressed()[pygame.K_d] != 0:
            ship.angle -= .1
            ship.renderangle -= 5.72957795
        if ship.x >= 800:
            ship.x = 1
        if ship.x <= 0:
            ship.x = 799
        if ship.y >= 600:
            ship.y = 1
        if ship.y <= 0:
            ship.y = 599
        score = font.render("{0}".format(game.score), True, white)
        gameover = font.render("{0}".format(game.gameover), True, white)
        ship.x -= math.sin(ship.angle) * ship.acceleration
        ship.y -= math.cos(ship.angle) * ship.acceleration
        if ship.acceleration >= 1:
            ship.acceleration *= 0.96
        if random.randint(0, 100) > 93:
            if random.random() > 0.5:
                if random.random() > 0.5:
                    asteroids.append([random.randint(0, 800), 0, random.randint(0, 7), False])
                else:
                    asteroids.append([random.randint(0, 800), 600, random.randint(0, 7), False])
            else:
                if random.random() > 0.5:
                    asteroids.append([0, random.randint(0, 600), random.randint(0, 7), False])
                else:
                    asteroids.append([800, random.randint(0, 600), random.randint(0, 7), False])
        for a in range(len(asteroids)):
            asteroids[a][0] -= math.sin(asteroids[a][2]) * 3
            asteroids[a][1] -= math.cos(asteroids[a][2]) * 3
        for a in range(len(asteroids)):
            for b in range(len(bullets)):
                if (math.fabs(bullets[b][0] - asteroids[a][0]) < 22) & (
                    math.fabs(bullets[b][1] - asteroids[a][1]) < 22):
                    bullets[b][3] = True
                    asteroids[a][3] = True
        for a in range(len(asteroids)):
            if (math.fabs(ship.x - asteroids[a][0]) < 22) & (math.fabs(ship.y - asteroids[a][1]) < 22):
                render(300, 285, gameover)
                render(400, 305, score)
                pygame.display.update()
                time.sleep(3)
                playing = False
        for a in range(len(asteroids)):
            if asteroids[a][0] >= 800:
                asteroids[a][0] = 1
            if asteroids[a][0] <= 0:
                asteroids[a][0] = 799
            if asteroids[a][1] >= 600:
                asteroids[a][1] = 1
            if asteroids[a][1] <= 0:
                asteroids[a][1] = 599
        for a in asteroids:
            if a[3] == True:
                asteroids.remove(a)
                game.score += 1
        for b in bullets:
            if b[3] == True:
                bullets.remove(b)
        for a in asteroids:
            render(a[0], a[1], asteroid.image)
        for b in bullets:
            render(b[0], b[1], bullet.image)
        for b in range(len(bullets)):
            bullets[b][0] -= math.sin(bullets[b][2]) * 14
            bullets[b][1] -= math.cos(bullets[b][2]) * 14
        for b in bullets:
            if b[0] < 0 or b[0] > 800 or b[1] < 0 or b[1] > 600:
                bullets.remove(b)
        render(ship.x, ship.y, rot_center(ship.sprite.image, ship.renderangle))
        render(10, 10, score)
    elif playing == False:
        ship.x = 400
        ship.y = 300
        ship.angle = 0
        ship.renderangle = 0
        ship.acceleration = 0
        game.score = 0
        bullets = []
        asteroids = []
        titletext = font.render("{0}".format(game.title), True, white)
        subtext = font.render("{0}".format(game.text), True, white)
        render(370, 270, titletext)
        render(325, 300, subtext)
    pygame.display.update()
    clock.tick(50)
    gameDisplay.fill(game.bgcolor)
pygame.quit()
quit()
