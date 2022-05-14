import var
import pyautogui
import pygame as pg
from shape import Shape
from cv2 import cv2 as cv
from random import choice,randint,random
from const import BACKGROUND,CAMERA,CLOCK,COLORS,FACE_DETECTOR,FONT,HEIGHT,PREDICTOR,SCREEN,WIDTH
# import module with variables and import pyautogui to make pop-ups
# import pygame with alias pg and import Shape class from shape module
# import module cv2 from open-cv with alias cv
# from random import choice to select a random item from a list,
# randint to generate a random number between an interval
# and random to generate a random number between 0 and 1
# import necessary constants from const module

def _camera_alert():

	"""Private function that displays a pop-up alert to let you know
	you need to stay in the front of the camera to start the game"""

	pyautogui.alert("Stay in front of the camera to start the game!")
	# alert player to stay in the front of the camera

def _hide_mouse():

	"""Private function that hides the cursor of the mouse"""

	pg.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
	# make the cursor of the mouse invisible

def _set_title():

	"""Private function that sets the title of the game"""

	pg.display.set_caption("Shadow Dragon")
	# set the title of the game

def _gray_frame():

	"""Private function that returns the grayscale of an image
	or displays a pop-up to let you know you don't have a camera"""

	try: return cv.cvtColor(CAMERA.read()[1],cv.COLOR_BGR2GRAY)
	except: pyautogui.alert("YOU DON'T HAVE A CAMERA!!!!!")
	# if the player have a webcam
	# convert the image from webcam to grayscale and return it
	# otherwise alerts the player that he doesn't have webcam

def _eye_info(landmark,number=1):

	"""Private function that return information about the eyes"""

	return (landmark.part(36).x,landmark.part(41).y-landmark.part(37).y) if number!=1 else landmark.part(36).x
	# return the point of the eye
	# if this function is called in _first_point function
	# otherwise return a tuple with the point of the eye
	# and the distance between top and bottom of the eye

def _first_point():

	"""Private function that returns first point of the eye"""

	while 1:
		for face in FACE_DETECTOR(g:=_gray_frame()): return _eye_info(PREDICTOR(g,face))
	# open-cv doesn't let you to catch a single frame from camera
	# so i need to do an infinite loop
	# loop the list with the detected faces in the grayscale image
	# and return the eye info when a face is found

def prepare_game():

	"""Function that prepares the game to be playable"""

	_camera_alert()
	# alert the player

	_hide_mouse()
	# hide the mouse

	_set_title()
	# set title

	return _first_point()
	# return eye's first point

def draw_screen():

	"""Function that draws the screen of the game"""

	SCREEN.blit(BACKGROUND,(0,0))
	# draw the background

	SCREEN.blit(FONT.render(f"Points: {var.points}  Lives: {var.lives}",True,(255,255,255)),(0,0))
	# write the points and the remaining lives

	SCREEN.blit(FONT.render(f"Fps: {int(CLOCK.get_fps())}",True,(255,255,255)),(WIDTH-HEIGHT/5,0))
	# write the fps

	pg.draw.rect(SCREEN,(0,0,0),var.player)
	# draw the player

def _stop_game():

	"""Private function that stops the game"""

	var.run=False
	# set the variable that track if the game is running or not to false

def _reset():

	"""Private function that resets the game"""

	var.points=0
	# set points again to 0

	var.chance=0.99
	# set the chance to default value

	var.lives=3
	# set the lives again to 3

	var.game=True
	# set the game variable to True

	var.player.x=WIDTH//2-WIDTH//14
	# reset the player position

def _switch_mute():

	"""Private function that switchs the value of mute variable"""

	var.mute=False if var.mute else True
	# switch the value of mute variable

def _switch_pause():

	"""Private function that switchs the value of pause variable"""

	var.pause=False if var.pause else True
	# switch the value of pause variable

def _search_key(event):

	"""Private function that searchs for key and starts its activity"""

	# if a key is pressed
	if event.type==pg.KEYDOWN:
		if event.key==pg.K_ESCAPE: _stop_game()
		# if esc key is pressed stop the game
		elif event.key==pg.K_SPACE and var.lives==0: _reset()
		# if the space key is pressed and the game is over reset the game
		elif event.key==pg.K_m: _switch_mute()
		# if the m key is pressed mute the game
		elif event.key==pg.K_p: _switch_pause()
		# if the p key is pressed pause the game

def handle_keys():

	"""Function that handles game's keys"""

	for event in pg.event.get(): _search_key(event)
	# loop the event list and search for pressing keys

def not_paused():

	"""Function that verifies is the game isn't paused"""

	return not var.pause
	# return if the game isn't paused

def _destroy(enemy):

	"""Private function that destroys an enemy"""

	var.enemies.remove(enemy)
	# remove the enemy from the enemies list

def _not_muted():

	"""Private function that verifies if the game isn't muted"""

	return not var.mute
	# return if the game isn't muted

def _play(sound):

	"""Private function that plays a song"""

	if _not_muted(): pg.mixer.Sound(f"D:/python$/pygame/ShadowDragon/sounds/{sound}").play()
	# if the game isn't muted play a specific song

def _check_destroy(enemy):

	"""Private function that checks if an enemy need to be destroyed"""

	# check if the enemy fell outside the game
	# and put this in a varible with walrus operator
	if c:=(enemy.y-enemy.size>=HEIGHT):
		_destroy(enemy)
		# destroy the enemy

		_play("miss.wav")
		# play the song for missing an enemy

	var.lives-=c
	# if the variable for checking if the enemy fell outside the game is true
	# decrease a life

def _calculate_points(enemy):

	"""Private function that calculates player's points"""

	if enemy.shape=="circle": var.points+=10
	# if the shape is circle add 10 points
	elif enemy.shape=="triangle": var.points+=100
	# if the shape is triangle add 100 points
	else: var.points+=1000
	# if the shape is square add 1000 points

def _hit(enemy):

	"""Private function that hits the enemy"""

	_destroy(enemy)
	# destroy the enemy

	_calculate_points(enemy)
	# calculate the points of player

def _collide(enemy):

	"""Private function that collides with enemy"""

	_play("points.wav")
	# play the song for gaining points
	_hit(enemy)
	# hit the enemy

def _check_collision(enemy):

	"""Private function that checks for collision"""

	return enemy.collision(var.player)
	# check if an enemy collide with player

def _collision(enemy):

	"""Private function that does a collision with enemy"""

	if _check_collision(enemy): _collide(enemy)
	# collide player with enemy it this happens

def _enemy_logic(enemy):

	"""Private function that does the enemy's logic"""

	# if the game isn't paused
	if not_paused():
		enemy.fall()
		# aply gravity to the enemy

		_check_destroy(enemy)
		# check if the enemy is destroyed

		_collision(enemy)
		# make a collision with enemy if is needed

def _handle_enemy(enemy):

	"""Private function that handles an enemy"""

	enemy.draw()
	# draw the enemy

	_enemy_logic(enemy)
	# do the enemy logic

def handle_enemies():

	"""Function that handles the enemies"""

	for enemy in var.enemies: _handle_enemy(enemy)
	# loop the list with enemies

def no_lives():

	"""Function that checks if the player ran out of lives"""

	return var.lives==0
	# return if the player ran out of lives

def _reset_enemies():

	"""Private function that resets the enemies"""

	var.enemies.clear()
	# clear the list with enemies

def _game_on():

	"""Private function that checks if the game is on"""

	return var.game
	# return if the game is on

def _end_game():

	"""Private function that ends the game"""

	var.game=False
	# set game variable to false

def game_over():

	"""Function that prepares ending of the game"""

	SCREEN.blit(t:=(FONT.render("Game Over!",True,(255,255,255))),t.get_rect(center=SCREEN.get_rect().center))
	# write the game over text in the center of the screen

	_reset_enemies()
	# reset enemies

	if _game_on(): _play("gameover.wav")
	# if game is on play the game over song

	_end_game()
	# end the game

def _move_left():

	"""Private function that moves the player to left"""

	var.player.x=var.player.x-var.player.w if var.player.x>var.player.w else var.player.x
	# move player one position to left

def _move_right():

	"""Private function that moves the player to right"""

	var.player.x=var.player.right if var.player.right+var.player.w<WIDTH else var.player.x
	# move player one position to right

def _move(eye_point,eye_distance,start_point):

	"""Private function that moves the player"""

	if eye_point-start_point>eye_distance and var.lives!=0: _move_left()
	# if the player eyes moved to left and player is still in game
	# move the player to left
	elif eye_point-start_point<-eye_distance and var.lives!=0: _move_right()
	# if the player eyes moved to right and player is still in game
	# move the player to right

def handle_cv(start_point):

	"""Function that handles the computer vision and the ai of the game"""

	# loop the list with the detected faces in the grayscale image
	for face in FACE_DETECTOR(g:=_gray_frame()):
		eye_point,eye_distance=_eye_info(PREDICTOR(g,face),2)
		# colect info about eyes in 2 variables

		_move(eye_point,eye_distance,start_point)
		# move player to the correct position

		return eye_point if var.iteration==0 else start_point
		# return new eye's point if eye's point need to be changed
		# otherwise the old point

	return start_point
	# if the loop wasn't be executed return the old point

def _check_spawn():

	"""Private function that checks if is needed to spawn a new enemy"""

	return random()>var.chance and var.lives!=0
	# return if a new enemy can be spawned

def _spawn_shape(shape):

	"""Private function that spawns a shape"""

	if shape=="circle": var.enemies.append(Shape(randint(WIDTH//35,WIDTH-HEIGHT//20),-HEIGHT//10,choice(COLORS),shape))
	elif shape=="triangle": var.enemies.append(Shape(randint(WIDTH//35,WIDTH-HEIGHT//20),-HEIGHT//10,choice(COLORS),shape))
	else: var.enemies.append(Shape(randint(WIDTH//35,WIDTH-HEIGHT//10),-HEIGHT//10,choice(COLORS),shape))
	# if the given shape is circle apend to enemies list a circle
	# if the given shape is triangle apend to enemies list a triangle
	# if the given shape is square apend to enemies list a square

def _spawn_specific_enemy():

	"""Private function that decides what enemy will spawn and spawn it"""

	if (n:=randint(0,99))<90: _spawn_shape("circle")
	elif 89<n<99: _spawn_shape("triangle")
	else: _spawn_shape("square")
	# spawn a spawn depending on the spawning chance

def spawn_enemy():

	"""Function that spawns an enemy"""

	if _check_spawn(): _spawn_specific_enemy()
	# spawn new enemy

def _update_chance():

	"""Private function that updates the chance to spawn an enemy"""

	var.chance-=0.0000000000000001
	# update the spawning chance of an enemy

def _set_iteration():

	"""Private function that changes the iteration"""

	var.iteration^=1
	# chance the iteration
	# i used bitwise XOR
	# if iteration is 0, XOR 1 will switch to 1
	# otherwise XOR 1 will switch to 0

def prepare_next_frame():

	"""Function that prepares the next frame of the game"""

	_update_chance()
	# update the spawning chance

	_set_iteration()
	# and set the iteration