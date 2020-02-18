import sys
import pygame
import time


black = 0, 0, 0 # obstacles
blue = 0, 0, 255 # path
yellow = 255, 255, 0 # start node
pink = 255, 51, 204 # target node
green = 0, 255, 0 # open nodes
red = 255, 0, 0 # closed nodes
white = 255, 255, 255 # normal nodes
blockSize = 40
width = 20
height = 15
margin = 1
size = 800, 600


# Constants:
# Node types:
NORMAL = 0
OBSTACLE = 1
START = 2
TARGET = 3
# modes:
OBSTACLES_DRAWING = 0
START_DRAWING = 1
TARGET_DRAWING = 2
SOLVING_MAZE = 3

mode = OBSTACLES_DRAWING



class Node:
    def __init__(self, x, y):
        self.type = NORMAL
        self.x = x
        self.y = y
        self.closed = False
        self.g_cost = 0  # distance from start
        self.h_cost = 0  # distance to target
        self.f_cost = 0  # g_cost + h_cost
        self.rect = pygame.Rect(x*blockSize + margin, y*blockSize +
                                margin, blockSize - 2*margin, blockSize - 2*margin)

    def drawNode(self):
        if self.type == NORMAL:
            pygame.draw.rect(screen, white, self.rect)
        if self.type == OBSTACLE:
            pygame.draw.rect(screen, black, self.rect)
        if self.type == START:
            pygame.draw.rect(screen, yellow, self.rect)
        if self.type == TARGET:
            pygame.draw.rect(screen, pink, self.rect)

    def setType(self, type):
        self.type = type


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[]]
        self.start_x = 0
        self.start_y = 0
        self.target_x = 0
        self.target_y = 0
        self.startNodeReady = False
        self.targetNodeReady = False
        for x in range(width):
            self.grid.append([])
            for y in range(height):
                self.grid[x].append(Node(x, y))

    def drawGrid(self):
        for x in range(self.width):
            for y in range(self.height):
                self.grid[x][y].drawNode()

    def setNodeType(self, x, y, type):
        if type == START:
            if self.startReady == True:
                self.grid[self.start_x][self.start_y].setType(NORMAL)
            self.start_x = x
            self.start_y = y
            self.startNodeReady = True
        elif type == TARGET:
            if self.targetReady == True:
                self.grid[self.target_x][self.target_y].setType(NORMAL)
            self.target_x = x
            self.target_y = y
            self.targetNodeReady = True

        self.grid[x][y].setType(type)

        if self.start_x == x and self.start_y == y and type != START:
            self.startNodeReady = False
        elif self.target_x and self.target_y == y and type != TARGET:
            self.targetNodeReady = False

pygame.init()
screen = pygame.display.set_mode(size)

buttonEvents = []
grid = Grid(width, height)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    grid.drawGrid()
    buttonEvents = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    x = int(mouse[0] / blockSize)
    y = int(mouse[1] / blockSize)

    if buttonEvents[pygame.K_1]:
        mode = OBSTACLES_DRAWING
    elif buttonEvents[pygame.K_2]:
        mode = START_DRAWING
    elif buttonEvents[pygame.K_3]:
        mode = TARGET_DRAWING


    if mode == OBSTACLES_DRAWING:
        if click[0] == 1:
            grid.setNodeType(x, y, OBSTACLE)
        if click[2] == 1:
            grid.setNodeType(x, y, NORMAL)

    if mode == START_DRAWING:
        if click[0] == 1:
            grid.setNodeType(x, y, START)
        if click[2] == 1:
            grid.setNodeType(x, y, NORMAL)

    if mode == TARGET_DRAWING:
        if click[0] == 1:
            grid.setNodeType(x, y, TARGET)
        if click[2] == 1:
            grid.setNodeType(x, y, NORMAL)



    time.sleep(0.03)
    pygame.display.update()
