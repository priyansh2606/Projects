import pygame
import math 
from queue import PriorityQueue

WIDTH = 800 #width of the block
WIN = pygame.display.set_mode((WIDTH, WIDTH))  #square of width by width makes a window 
pygame.display.set_caption("A* Path Finding Algorithm") #title

#RGB INTENSITY OF COLOURS 255 is max  and 0 is min
#it is in form of tuples 
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

#to get position on the grid create class  
class Spot:
	def __init__(self, row, col, width, total_rows): #constructor that takes 5 arg
		self.row = row  #row: The row of the spot on the grid.
		self.col = col  #col: The column of the spot on the grid.
		self.x = row * width  #x: The X-coordinate of the spot on the grid.
		self.y = col * width  #y: The Y-coordinate of the spot on the grid.
		self.color = WHITE  #color: The color of the spot.
		self.neighbors = []  #neighbors: A list of the spot's neighbors on the grid.
		self.width = width  #width: The width of each spot on the grid.
		self.total_rows = total_rows  #total_rows: The total number of rows in the grid.

	def get_pos(self): #returns position of the block
		return self.row, self.col

	#red colour for inside cubes
	def is_closed(self):
		return self.color == RED
	#green outline
	def is_open(self):
		return self.color == GREEN
	#for barrier colour is black
	def is_barrier(self):
		return self.color == BLACK
	#start cubes is orange
	def is_start(self):
		return self.color == ORANGE
	#end is purple
	def is_end(self):
		return self.color == TURQUOISE

 	#to reset game its white 
	def reset(self):
		self.color = WHITE

	#again make the game and start with the orange 
	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	#to make the path path colour
	def make_path(self):
		self.color = PURPLE

	#function to draw the rectangle  
	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
     
        
	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #moving down
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # moving up
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # moving right
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # moving left
			self.neighbors.append(grid[self.row][self.col - 1])
   
	#takes self and other argument compares it 
	def __lt__(self, other):
		return False

#define the h function here
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

#to construct the path for the final shortest distance
def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

#the main algo of A*
def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()#gives the min element from the travel
	open_set.put((0, count, start))#add the score at 1st node
	came_from = {}#where the 1st node is 
 #defining g score and f score for the algo initially both g=0
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()
		draw()

		if current != start:
			current.make_closed()

	return False

#to make the grid 
def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows) #creates the new spot 
			grid[i].append(spot)

	return grid #return the grid of spot objects

#to draw the particular grid from top to bottom for traversing
def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))
   
def draw(win, grid, rows, width):
	win.fill(WHITE) #to make the grid full of white cubes

	for row in grid:
		for spot in row: 
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()

#to define which cube will have which colour like 1st is orange 
def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

#main function to make the grid and display oe call the functions 
def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # leftclick changes direction of dot
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end: #if not yet started 1st dot will be the start
					start = spot			#start and end should not be equal
					start.make_start()

				elif not end and spot != start:#make the last dot
					end = spot
					end.make_end()

				elif spot != end and spot != start:#make barrier
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # rightclick of mouse
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:#to clear for reset the game
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()
main(WIN, WIDTH)