import pygame as pg
from const import HEIGHT,WIDTH
# import pygame with alias pg and import necessary constants from const module

# int variables

iteration=0
points=0
chance=0.99
lives=3
# variables for iteration of the game, player points, chance to spawn enemies
# and lives of the player

# bool variables

mute=False
pause=False
game=True
run=True
# variables for tracking if the game is muted, paused, on or running

# list variables

enemies=[]
# list variable with all the enemies

# object variables

player=pg.Rect(WIDTH//2-WIDTH//14,HEIGHT//15*12.5,WIDTH//7,HEIGHT//15)
# variable with player with specifications:
# x coordinate of up left corner: half of the screen width
# minus half of the player width
# y coordinate of up left corner: a fifteenth of the height of the screen
# multiply with twelf and a half
# player width: a seventh of the screen width
# player height: a fifteenth of the height of the screen