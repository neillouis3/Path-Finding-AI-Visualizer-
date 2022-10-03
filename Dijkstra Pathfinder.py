from tkinter import messagebox, Tk
import pygame
import sys

windowWidth = 500
windowHeight = 500
window = pygame.display.set_mode((windowWidth, windowHeight))

pygame.display.set_caption("Path Finding Visualizer")

columns = 25
rows = 25
boxWidth = windowWidth // columns
boxHeight = windowHeight // rows

grid = []
queue = []
path = []


class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * boxWidth, self.y * boxHeight, boxWidth - 2, boxHeight - 2))

    def setNeighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])


for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)

for i in range(columns):
    for j in range(rows):
        grid[i][j].setNeighbours()


def main():
    startSearch = False
    targetBoxSet = False
    startBoxSet = False
    searching = True
    targetBox = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                if event.buttons[0]:
                    if startBoxSet:
                        i = x // boxWidth
                        j = y // boxHeight
                        grid[i][j].wall = True
                    else:
                        i = x // boxWidth
                        j = y // boxHeight
                        startBox = grid[i][j]
                        startBox.start = True
                        startBoxSet = True
                        startBox.visited = True
                        queue.append(startBox)

                if event.buttons[2] and not targetBoxSet:
                    i = x // boxWidth
                    j = y // boxHeight
                    targetBox = grid[i][j]
                    targetBox.target = True
                    targetBoxSet = True
            if event.type == pygame.KEYDOWN and targetBoxSet:
                startSearch = True

        if startSearch:
            if len(queue) > 0 and searching:
                currentBox = queue.pop(0)
                currentBox.visited = True
                if currentBox == targetBox:
                    searching = False
                    while currentBox.prior != startBox:
                        path.append(currentBox.prior)
                        currentBox = currentBox.prior
                else:
                    for neighbour in currentBox.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = currentBox
                            queue.append(neighbour)

            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No solution", "There is no solution")
                    searching = False

        window.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (50, 50, 50))

                if box.queued:
                    box.draw(window, (200, 0, 0))
                if box.visited:
                    box.draw(window, (0, 200, 0))
                if box in path:
                    box.draw(window, (0, 0, 200))
                if box.start:
                    box.draw(window, (0, 200, 200))
                if box.wall:
                    box.draw(window, (90, 90, 90))
                if box.target:
                    box.draw(window, (200, 200, 0))


        pygame.display.update()

main()