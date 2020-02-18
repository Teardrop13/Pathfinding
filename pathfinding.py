import sys
import pygame
import time

# Node modes:
# 0 - normal
# 1 - obstacle
# 2 - start
# 3 - target

black = 0, 0, 0
blue = 0, 0, 255
green = 0, 255, 0 
red = 255, 0, 0
white = 255, 255, 255
blockSize = 40
width = 20
height = 15
margin = 1
size = 800, 600

pygame.init()
screen = pygame.display.set_mode(size)

class Node:
    def __init__(self, x, y):
        self.mode = 0
        self.x = x
        self.y = y
        self.closed = False
        # distance from start
        self.g_cost = 0
        # distance to target
        self.h_cost = 0
        # g_cost + h_cost
        self.f_cost = 0
        self.rect = pygame.Rect(x*blockSize + margin, y*blockSize + margin, blockSize - 2*margin, blockSize - 2*margin)

    def drawRect(self):
        if self.mode == 0:
            pygame.draw.rect(screen, white, self.rect)
        if self.mode == 1:
            pygame.draw.rect(screen, blue, self.rect)
        if self.mode == 2:
            pygame.draw.rect(screen, red, self.rect)
        if self.mode == 3:
            pygame.draw.rect(screen, green, self.rect)

    def setMode(self, mode):
        self.mode = mode


array = [[]]
for x in range(width):
    array.append([])
    for y in range(height):
        array[x].append(Node(x, y))

buttonEvents = []

buttonEvents = pygame.key.get_pressed()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    for x in range(width):
        array.append([])
        for y in range(height):
            array[x][y].drawRect()
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    x = int(mouse[0] / blockSize)
    y = int(mouse[1] / blockSize)
    if click[0] == 1:
        array[x][y].setMode(1)
    time.sleep(0.05)
    pygame.display.update()