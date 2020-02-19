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
# Node possible states:
UNVERIFIED = 0
OPENED = 1
CLOSED = 2
# modes:
OBSTACLES_DRAWING = 0
START_DRAWING = 1
TARGET_DRAWING = 2
SOLVING_MAZE = 3


vectors = {(0, -1), (1, -1), (1, 0), (1, 1),
           (0, 1), (-1, 1), (-1, 0), (-1, -1)}

mode = OBSTACLES_DRAWING


class Node:
    def __init__(self, x, y, screen):
        self.myfont = pygame.font.SysFont('Arial', 15)
        self.screen = screen
        self.type = NORMAL
        self.x = x
        self.y = y
        self.state = UNVERIFIED
        self.g_cost = 0  # distance from start
        self.h_cost = 0  # distance to target
        self.f_cost = 0  # g_cost + h_cost
        self.rect = pygame.Rect(x*blockSize + margin, y*blockSize +
                                margin, blockSize - 2*margin, blockSize - 2*margin)

    def drawNode(self):
        if self.type == NORMAL:
            if self.state == CLOSED:
                pygame.draw.rect(screen, red, self.rect)
                text = self.myfont.render(str(self.f_cost), False, (0,0,0))
                self.screen.blit(text,(self.x*40 + 10,self.y*40 + 10))
            elif self.state == OPENED:
                pygame.draw.rect(screen, green, self.rect)
                text = self.myfont.render(str(self.f_cost), False, (0,0,0))
                self.screen.blit(text,(self.x*40 + 10,self.y*40 + 10))
            else:     
                pygame.draw.rect(screen, white, self.rect)
        if self.type == OBSTACLE:
            pygame.draw.rect(screen, black, self.rect)
        if self.type == START:
            pygame.draw.rect(screen, yellow, self.rect)
        if self.type == TARGET:
            pygame.draw.rect(screen, pink, self.rect)

    def setType(self, type):
        self.type = type

    def isClosed(self):
        return self.state

    def close(self):
        self.state = CLOSED

    def setCosts(self, g_cost, h_cost):
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost


class Grid:
    vectors = {(0, -1), (1, -1), (1, 0), (1, 1),
           (0, 1), (-1, 1), (-1, 0), (-1, -1)}
    def __init__(self, width, height, screen):
        self.screen = screen
        self.width = width
        self.height = height
        self.grid = [[]]
        self.start_x = 0
        self.start_y = 0
        self.target_x = 0
        self.target_y = 0
        self.openedNodes = [] # list of closest opened nodes
        self.startNodeReady = False
        self.targetNodeReady = False
        for x in range(width):
            self.grid.append([])
            for y in range(height):
                self.grid[x].append(Node(x, y, self.screen))

    def drawGrid(self):
        for x in range(self.width):
            for y in range(self.height):
                self.grid[x][y].drawNode()

    def setNodeType(self, x, y, type):
        if type == START:
            if self.startNodeReady == True:
                self.grid[self.start_x][self.start_y].setType(NORMAL)
            self.start_x = x
            self.start_y = y
            self.startNodeReady = True
        elif type == TARGET:
            if self.targetNodeReady == True:
                self.grid[self.target_x][self.target_y].setType(NORMAL)
            self.targetNodeReady = True
            self.target_x = x
            self.target_y = y
        elif type == OBSTACLE:
            self.grid[x][y].state = CLOSED
        else:
            self.grid[x][y].state = UNVERIFIED
            
        self.grid[x][y].setType(type)

        if self.start_x == x and self.start_y == y and type != START:
            self.startNodeReady = False
        elif self.target_x and self.target_y == y and type != TARGET:
            self.targetNodeReady = False

    def findLowest_f_cost_nodes(self):
        # returns list of coordinates of nodes
        # return type list of tuples
 
        lowest_f_cost = self.grid[self.openedNodes[0][0]][self.openedNodes[0][1]].f_cost
        listOfNodes = []

        for node in self.openedNodes:
            if self.grid[node[0]][node[1]].f_cost < lowest_f_cost:
                listOfNodes.clear()
                listOfNodes.append((node[0],node[1]))
                lowest_f_cost = self.grid[node[0]][node[1]].f_cost
            elif self.grid[node[0]][node[1]].f_cost == lowest_f_cost:
                listOfNodes.append((node[0],node[1]))

        return listOfNodes


    def calculate_h_cost(self, x, y):
        horizontalDistance = abs(self.target_x - x)
        verticalDistance = abs(self.target_y - y)

        straightDistance = abs(horizontalDistance - verticalDistance)
        diagonalDistance = abs(max(horizontalDistance, verticalDistance) - straightDistance)

        return 10*straightDistance + 14*diagonalDistance


    def pathfinding(self):
        current_x = self.start_x
        current_y = self.start_y
        self.openedNodes = [(current_x, current_y)]
        while current_x != self.target_x or current_y != self.target_y:      
            listOfNodes = self.findLowest_f_cost_nodes()
            for node in listOfNodes:
                current_x = node[0]
                current_y = node[1]
                for vector in vectors:
                    if current_x+vector[0] in range(0, width) and current_y+vector[1] in range(0, height):
                        if self.grid[current_x+vector[0]][current_y+vector[1]].state != CLOSED:
                            if vector[0] != 0 or vector[1] != 0:
                                added_g_cost = 14
                            else:
                                added_g_cost = 10
                            g_cost = self.grid[current_x][current_y].g_cost + added_g_cost
                            h_cost = self.calculate_h_cost(current_x+vector[0], current_y+vector[1])

                            if g_cost + h_cost < self.grid[current_x+vector[0]][current_y+vector[1]].f_cost or self.grid[current_x+vector[0]][current_y+vector[1]].f_cost == 0:
                                self.grid[current_x+vector[0]][current_y+vector[1]].setCosts(g_cost, h_cost)
                                self.openedNodes.append((current_x+vector[0], current_y+vector[1]))
                                self.grid[current_x+vector[0]][current_y+vector[1]].state = OPENED
                self.openedNodes.remove((current_x, current_y))
                self.grid[current_x][current_y].state = CLOSED

            self.drawGrid()
            time.sleep(0.2)
            pygame.display.update()
        return True


    def drawPath(self):
        current_x = self.target_x
        current_y = self.target_y
        prev_current_x = self.target_x
        prev_current_y = self.target_y
        shortestPath = []
        while current_x != self.start_x or current_y != self.start_y:
            lowest_f_cost = self.grid[current_x+1][current_y].f_cost
            lowest_f_cost_cords = (current_x+1, current_y)
            for vector in vectors:
                if self.grid[current_x+vector[0]][current_y+vector[1]].f_cost <= lowest_f_cost:
                    if current_x != prev_current_x and current_y != prev_current_y:
                        lowest_f_cost = self.grid[current_x+vector[0]][current_y+vector[1]].f_cost
                        lowest_f_cost_cords = (current_x+vector[0], current_y+vector[1])
            shortestPath.append(lowest_f_cost_cords)


        
        
        self.drawGrid()
        pygame.display.update()


pygame.init()
screen = pygame.display.set_mode(size)
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 6)

buttonEvents = []
grid = Grid(width, height, screen)

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

    if mode == SOLVING_MAZE:
        grid.pathfinding()
        #grid.drawPath()
        mode = OBSTACLES_DRAWING
        


    time.sleep(0.03)
    pygame.display.update()
