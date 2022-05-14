import var
import pygame as pg
from const import CLOCK
from func import draw_screen,game_over,handle_cv,handle_enemies,handle_keys,no_lives,not_paused,prepare_game,prepare_next_frame,spawn_enemy
# import module with variables and import pygame with alias pg
# import necessary constants from const module
# import all necessary functions from func module

start_point=prepare_game()
# set the first location of the right part of left eye
# and prepare the game

# start the main loop of the game
while var.run:
	CLOCK.tick(30)
	# set max number of fps to 30

	draw_screen()
	# draw the screen

	handle_keys()
	# handle the keys

	handle_enemies()
	# handle the enemies

	# if the game isn't paused
	if not_paused():
		if no_lives(): game_over()
		# if the player lost all his lives finish the game

		start_point=handle_cv(start_point)
		# update the start point

		spawn_enemy()
		# spawn an enemy

		prepare_next_frame()
		# prepare the next frame of the game

	pg.display.flip()
	# update the screen