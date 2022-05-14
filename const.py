import dlib
import pygame as pg
from cv2 import cv2 as cv
# import dlib to get detect faces and to get the landmark of a face
# import pygame with alias pg and import module cv2 from open-cv with alias cv

# pygame stuff

pg.init()
# initialise pygame

HEIGHT,WIDTH=pg.display.Info().current_h,pg.display.Info().current_w
# 2 constants with height and width of the screen

BACKGROUND=pg.transform.scale(pg.image.load("D:/python$/pygame/ShadowDragon/assets/background.jpg"),(WIDTH,HEIGHT))
# load the background, scale it to the screen size and put it in a constant

CLOCK=pg.time.Clock()
# constant with a clock

FONT=pg.font.Font("freesansbold.ttf",HEIGHT//20)
# constant with the font

SCREEN=pg.display.set_mode((WIDTH,HEIGHT))
# constant with the screen

# open-cv and dlib stuff

CAMERA=cv.VideoCapture(0)
# constant with the webcam

FACE_DETECTOR=dlib.get_frontal_face_detector()
# constant with the detector for faces

PREDICTOR=dlib.shape_predictor("D:/python$/pygame/ShadowDragon/data/shape_predictor_68_face_landmarks.dat")
# constant for landmark predictor

# other stuff

COLORS=[
(255,17,0), # red
(255,98,0), # orange
(255,196,0),# yellow
(140,255,0),# lime
(0,255,132),# green
(0,255,234),# cyan
(0,140,255),# blue
(17,0,255), # dark blue
(132,0,255),# purple
(255,0,230) # pink
]
# list with the colors of enemies
