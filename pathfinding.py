import sys
import pygame
import time

# 0 - normalne
# 1 - przeszkoda
# 2 - start
# 3 - koniec

black = 0, 0, 0
blue = 0, 0, 255
blockSize = 40
width = 20
height = 15
size = 800, 600

pygame.init()
screen = pygame.display.set_mode(size)

class Field:
    def __init__(self, x, y):
        self.type = 0
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x*blockSize, y*blockSize, blockSize, blockSize)

    def drawRect(self):
        pygame.draw.rect(screen, blue, self.rect)


array = []
for i in range(width):
    for k in range(height):
        array.append(Field(i, k))

buttonEvents = []

buttonEvents = pygame.key.get_pressed()

for i in array:
    i.drawRect()
    time.sleep(0.1)
    pygame.display.update()

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        sys.exit()