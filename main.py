import pygame
from pygame.locals import *

pygame.init()

#width and height of frame
screen_width = 600
screen_height = 500


fpsClock = pygame.time.Clock() #used to control game's framerate
screen = pygame.display.set_mode((screen_width, screen_height)) #setting the screen to the width and height set earlier
pygame.display.set_caption('Ping Pong') 


#defining and setting font size
font = pygame.font.SysFont('agencyfb', 30)


#defining variables
margin = 50
player1_score = 0
player2_score = 0
fps = 60
live_ball = False
winner = 0
acceleration = 0


#defining colors used throughout program
bg = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

#draws the background of the game
def draw_board():
	screen.fill(bg)
	pygame.draw.line(screen, white, (0, margin), (screen_width, margin), 2)


#used to write text onto the game frame
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#defining a paddle class
class paddle():
	#constructor
	def __init__(self, x, y): 
		self.x = x
		self.y = y
		self.rect = Rect(x, y, 20, 100)
		self.speed = 6

	#movement for player 1
	def p1Movement(self):
		key = pygame.key.get_pressed()
		if key[pygame.K_w] and self.rect.top > margin: #using w to move up and setting boundries for how high the paddle can go
			self.rect.move_ip(0, -1 * self.speed)
		if key[pygame.K_s] and self.rect.bottom < screen_height: #using s to move down and setting boundries for how low the paddle can go
			self.rect.move_ip(0, self.speed)

	#movement for player 2
	def p2Movement(self):
		key = pygame.key.get_pressed()
		if key[pygame.K_UP] and self.rect.top > margin: #using up arrow key to move up and setting boundries for how high the paddle can go
			self.rect.move_ip(0, -1 * self.speed)
		if key[pygame.K_DOWN] and self.rect.bottom < screen_height: #using down arrow key to move down and setting boundries for how low the paddle can go
			self.rect.move_ip(0, self.speed)

	#method to draw the paddle object onto the frame
	def draw(self):
		pygame.draw.rect(screen, white, self.rect)

#defining a ball class
class ball():
	#constructor
	def __init__(self, x, y):
		self.reset(x, y)

	#movement of the ball
	def move(self):

		#check collision with top margin
		if self.rect.top < margin:
			self.speed_y *= -1
		#check collision with bottom of the screen
		if self.rect.bottom > screen_height:
			self.speed_y *= -1
		if self.rect.colliderect(player2_paddle) or self.rect.colliderect(player1_paddle):
			self.speed_x *= -1

		#check for out of bounds
		if self.rect.left < 0:
			self.winner = 1
		if self.rect.left > screen_width:
			self.winner = -1

		#update ball position
		self.rect.x += self.speed_x
		self.rect.y += self.speed_y

		return self.winner

	#drawing the ball object onto the game frame
	def draw(self):
		pygame.draw.circle(screen, red, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)


	def reset(self, x, y):
		self.x = x
		self.y = y
		self.ball_rad = 8
		self.rect = Rect(x, y, self.ball_rad * 2, self.ball_rad * 2)
		self.speed_x = -4
		self.speed_y = 4
		self.winner = 0


#create paddles
player1_paddle = paddle(20, screen_height // 2)
player2_paddle = paddle(screen_width - 40, screen_height // 2)

#create pong ball
pong = ball(screen_width - 60, screen_height // 2 + 50)


#create game loop
run = True
while run:

	fpsClock.tick(fps)

	draw_board()
	draw_text('P1: ' + str(player1_score), font, white, 20, 15)
	draw_text('P2: ' + str(player2_score), font, white, screen_width - 60, 15)

	#draw paddles
	player1_paddle.draw()
	player2_paddle.draw()

	if live_ball == True:
		acceleration += 1
		winner = pong.move()
		if winner == 0:
			#draw ball
			pong.draw()
			#move paddles
			player1_paddle.p1Movement()
			player2_paddle.p2Movement()
		else:
			live_ball = False
			if winner == 1:
				player2_score += 1
			elif winner == -1:
				player1_score += 1


	#print player instructions
	if live_ball == False:
		if winner == 0:
			draw_text('CLICK ANYWHERE TO START', font, white, 160, screen_height // 2 -100)
		if winner == -1:
			draw_text('Player 1 SCORED!', font, white, 220, screen_height // 2 -100)
			draw_text('CLICK ANYWHERE TO START', font, white, 160, screen_height // 2 -50)
		if winner == 1:
			draw_text('Player 2 SCORED!', font, white, 220, screen_height // 2 -100)
			draw_text('CLICK ANYWHERE TO START', font, white, 160, screen_height // 2 -50)



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
			live_ball = True
			pong.reset(screen_width - 60, screen_height // 2 + 50)



	if acceleration > 500:
		acceleration = 0
		if pong.speed_x < 0:
			pong.speed_x -= 1
		if pong.speed_x > 0:
			pong.speed_x += 1
		if pong.speed_y < 0:
			pong.speed_y -= 1
		if pong.speed_y > 0:
			pong.speed_y += 1


	pygame.display.update()

pygame.quit()