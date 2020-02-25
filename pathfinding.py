import sys
import time

import pygame


black = 0, 0, 0  # obstacles
blue = 0, 0, 255  # path
yellow = 255, 255, 0  # start node
pink = 255, 51, 204  # target node
green = 0, 255, 0  # open nodes
red = 255, 0, 0  # closed nodes
white = 255, 255, 255  # normal nodes

blockSize = 40
margin = 1  # distance between squeres
width = 20
height = 15
size = 800, 600

# Constants:
# Node types:
NORMAL = 0
OBSTACLE = 1
START = 2
TARGET = 3
# Node possible states:
UNVERIFIED = 0
OPENED = 1
CLOSED = 2
IN_PATH = 3
# modes:
OBSTACLES_DRAWING = 0
START_DRAWING = 1
TARGET_DRAWING = 2
SOLVING_MAZE = 3

mode = OBSTACLES_DRAWING

vectors = {(0, -1), (1, -1), (1, 0), (1, 1),
           (0, 1), (-1, 1), (-1, 0), (-1, -1)}


class Node:
    '''
    Nodes that are not obstacles and have been already checked 
    for lowest f_cost have f_cost written on them.

    Node possible states:
    UNVERIFIED - Node that hasnt been considered yet, white color on visualisation
    OPENED - Node that could have lower f_cost, green
    CLOSED - considered and has lowest possible f_cost, red
    IN_PATH - state needed only for redrawing grid after path has been found, blue
    '''

    def __init__(self, x, y, screen, font):
        self.myfont = font
        self.screen = screen
        self.type = NORMAL
        self.color = white
        self.x = x
        self.y = y
        self.previousNode = (0, 0)
        self.state = UNVERIFIED
        self.g_cost = 0  # distance from start
        self.h_cost = 0  # distance to target
        self.f_cost = 0  # g_cost + h_cost
        self.rect = pygame.Rect(x*blockSize + margin, y*blockSize +
                                margin, blockSize - 2*margin, blockSize - 2*margin)

    def setColor(self):
        # Sets color automaticly depending on type and state 
        if self.type == NORMAL:
            if self.state == CLOSED:
                return red
            elif self.state == OPENED:
                return green
            elif self.state == IN_PATH:
                return blue
            else:
                return white
        elif self.type == OBSTACLE:
            return black
        elif self.type == START:
            return yellow
        elif self.type == TARGET:
            return pink

    def drawNode(self):
        self.color = self.setColor()
        pygame.draw.rect(screen, self.color, self.rect)

        if self.state in (OPENED, CLOSED, IN_PATH):
            text = self.myfont.render(str(self.f_cost), False, (0, 0, 0))
            self.screen.blit(text, (self.x*40 + 10, self.y*40 + 10))

    def setCosts(self, g_cost, h_cost):
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost


class Grid:
    '''
    It's a wrapper of 2d list of nodes
    '''
    def __init__(self, width, height, screen, font):
        self.screen = screen
        self.myfont = font

        self.width = width
        self.height = height
        self.grid = [[]]

        # Start and target coordinates when the ...ready flags are set False
        self.start_x = 0
        self.start_y = 0
        self.target_x = 0
        self.target_y = 0
        self.startNodeReady = False
        self.targetNodeReady = False

        self.openedNodes = []

        for x in range(width):
            self.grid.append([])
            for y in range(height):
                self.grid[x].append(Node(x, y, self.screen, self.myfont))

    def drawGrid(self):
        for x in range(self.width):
            for y in range(self.height):
                self.grid[x][y].drawNode()
        pygame.display.update()

    def clearGrid(self):
        self.grid.clear()
        self.openedNodes.clear()

        self.start_x = 0
        self.start_y = 0
        self.target_x = 0
        self.target_y = 0
        self.startNodeReady = False
        self.targetNodeReady = False

        self.openedNodes.clear()

        for x in range(width):
            self.grid.append([])
            for y in range(height):
                self.grid[x].append(Node(x, y, self.screen, self.myfont))

    def setNodeType(self, x, y, type):
        if type == START:
            if self.startNodeReady == True:
                self.grid[self.start_x][self.start_y].type = NORMAL
            self.startNodeReady = True
            self.start_x = x
            self.start_y = y
        elif type == TARGET:
            if self.targetNodeReady == True:
                self.grid[self.target_x][self.target_y].type = NORMAL
            self.targetNodeReady = True
            self.target_x = x
            self.target_y = y
        elif type == OBSTACLE:
            self.grid[x][y].state = CLOSED
        else:
            self.grid[x][y].state = UNVERIFIED

        self.grid[x][y].type = type

        if self.start_x == x and self.start_y == y and type != START:
            self.startNodeReady = False
        elif self.target_x == x and self.target_y == y and type != TARGET:
            self.targetNodeReady = False

    def resetNodes(self):
        '''
        Reset nodes to the initial state. Necessery for rerunning visualisation.
        '''
        for x in range(width):
            for y in range(height):
                if self.grid[x][y].type != OBSTACLE:
                    self.grid[x][y].state = UNVERIFIED
                self.grid[x][y].previousNode = (0, 0)
                self.grid[x][y].h_cost = 0
                self.grid[x][y].g_cost = 0
                self.grid[x][y].f_cost = 0

    def findLowest_f_cost_nodes(self):
        '''
        Returns list of coordinates of nodes
        Return type: list of tuples
        '''
        lowest_f_cost = self.grid[self.openedNodes[0][0]][self.openedNodes[0][1]].f_cost
        listOfNodes = []

        for node in self.openedNodes:
            if self.grid[node[0]][node[1]].f_cost < lowest_f_cost:
                listOfNodes.clear()
                listOfNodes.append((node[0], node[1]))
                lowest_f_cost = self.grid[node[0]][node[1]].f_cost
            elif self.grid[node[0]][node[1]].f_cost == lowest_f_cost:
                listOfNodes.append((node[0], node[1]))

        return listOfNodes

    def calculate_h_cost(self, x, y):
        '''
        Distance to target. Doesn't consider obstacles.
        10 - distance in straight line
        14 - diagonal distance
        '''
        horizontalDistance = abs(self.target_x - x)
        verticalDistance = abs(self.target_y - y)

        straightDistance = abs(horizontalDistance - verticalDistance)
        diagonalDistance = abs(max(horizontalDistance, verticalDistance) - straightDistance)

        return 10*straightDistance + 14*diagonalDistance

    def pathfinding(self):
        '''
        Main algorithm. Calculates f_costs until it finds target node.
        Returns True when the path is found, False otherwise.
        '''
        current_x = self.start_x
        current_y = self.start_y
        self.openedNodes = [(current_x, current_y)]

        while current_x != self.target_x or current_y != self.target_y:
            listOfNodes = self.findLowest_f_cost_nodes()
            for node in listOfNodes:
                current_x = node[0]
                current_y = node[1]
                for vector in vectors:

                    # Coordinates of node that will be considered in this iteration
                    x = current_x+vector[0]
                    y = current_y+vector[1]

                    if x in range(0, width) and y in range(0, height):
                        if self.grid[x][y].state != CLOSED:
                            if vector[0] == 0 or vector[1] == 0:
                                added_g_cost = 10
                            else:
                                added_g_cost = 14
                            g_cost = self.grid[current_x][current_y].g_cost + added_g_cost
                            h_cost = self.calculate_h_cost(x, y)
                            if g_cost + h_cost < self.grid[x][y].f_cost or self.grid[x][y].f_cost == 0:
                                self.grid[x][current_y + vector[1]].setCosts(g_cost, h_cost)
                                self.grid[x][current_y + vector[1]].previousNode = (current_x, current_y)
                                self.openedNodes.append((x, y))
                                self.grid[x][y].state = OPENED

                self.openedNodes.remove((current_x, current_y))
                self.grid[current_x][current_y].state = CLOSED
                if len(self.openedNodes) == 0:
                    self.drawGrid()
                    return False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.drawGrid()
            time.sleep(0.05)

        return True

    def drawPath(self):
        '''
        Marks 'IN_PATH' nodes that have lowest f_costs. Goes recursivly through nodes 
        starting from the target node.
        '''
        previousNode = self.grid[self.target_x][self.target_y].previousNode
        while previousNode[0] != self.start_x or previousNode[1] != self.start_y:
            self.grid[previousNode[0]][previousNode[1]].state = IN_PATH
            previousNode = self.grid[previousNode[0]][previousNode[1]].previousNode


pygame.init()
screen = pygame.display.set_mode(size)
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 15)

grid = Grid(width, height, screen, myfont)

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
    elif buttonEvents[pygame.K_4]:
        mode = SOLVING_MAZE
    elif buttonEvents[pygame.K_0]:
        grid.clearGrid()

    if mode == OBSTACLES_DRAWING:
        if click[0] == 1:
            grid.setNodeType(x, y, OBSTACLE)
        if click[2] == 1:
            grid.setNodeType(x, y, NORMAL)

    elif mode == START_DRAWING:
        if click[0] == 1:
            grid.setNodeType(x, y, START)
        if click[2] == 1:
            grid.setNodeType(x, y, NORMAL)

    elif mode == TARGET_DRAWING:
        if click[0] == 1:
            grid.setNodeType(x, y, TARGET)
        if click[2] == 1:
            grid.setNodeType(x, y, NORMAL)

    elif mode == SOLVING_MAZE:
        grid.resetNodes()  # Required for rerun algorithm purpose
        if grid.pathfinding():
            grid.drawPath()
        mode = OBSTACLES_DRAWING

    time.sleep(0.03)
