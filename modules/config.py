import pygame
import numpy as np
import math
import cv2
from dependencies.pantograph import Pantograph
from dependencies.pyhapi import Board, Device, Mechanisms
import sys, serial
from serial.tools import list_ports
import time
from PyQt5.QtWidgets import QApplication
import json
import os

def get_pixels(pm, image, pos_image):
    '''Returns rgb value of pixel on which mouse
       is currently positioned in assigned image
    '''
    rows, cols, _ = np.shape(image)

    pm = pm -  pos_image
    x,y = pm

    x,y = int(x), int(y)

    colors = []
    if x >= 0 and x < cols and y >= 0 and y < rows:
        colors = [image[y,x,:]]

    if len(colors) == 0: return_colors = [0,0,0]
    else: return_colors = colors[0].tolist()
        
    return return_colors

# Screen dimensions
screen_width  = 700
screen_height = 600
screen_dimensions = [screen_width, screen_height]

# Set FPS
FPS = 100
dt  = 1/FPS

# Tool size for tartar removal
tool_radius = 5

## Colors
background_color = (255, 255, 255)      # Set background color to green
inside           = [232, 162, 0]        # Color of gums
tartar_color     = [148, 127, 255]

# Load images
jaw_image    = pygame.image.load("images/lower_jaw_rotated2.png")
tartar_image = pygame.image.load("images/realistic_tartar_rotated.png")
tartar_image_2 = pygame.image.load("images/tartar_detection_rotated_2.png")

sprite       = cv2.imread('images/rotated_teeth_contour.png')
tartar       = cv2.imread('images/tartar_detection_rotated_2.png')
tartar       = cv2.cvtColor(tartar, cv2.COLOR_BGR2RGB)

# Calculate number of pixels that make up tartar
nr_tartar_pixels = 0
for i, row in enumerate(tartar):
    for j, pixel in enumerate(row):
        if np.all([tartar[i,j,k] == tartar_color[k] for k in range(3)]):
            nr_tartar_pixels += 1

# Store properties of ellipses to represent teeth (x,y,width,height)
teeth_ellipsoids = [[-2.9, 413.1, 122.9, 114.3],
                    [0, 314.3, 122.9, 114.3],
                    [29.4, 229.5, 103, 95.4],
                    [68.1, 152.2, 87.3, 87.8],
                    [129.3, 108.9, 59.6, 61.8],
                    [180.7, 77.5, 63.5, 60.2],
                    [240.9, 60.9, 65.1, 60.2],
                    [302, 60.9, 65.1, 60.2],
                    [362.1, 77.1, 65.1, 60.2],
                    [417.8, 108.4, 65.1, 60.2],
                    [450.4, 151.4, 89.2, 87.3],
                    [479.3, 225, 98.3, 99.4],
                    [487.5, 311.3, 117.3, 120.2],
                    [487.5, 413.1, 114.3, 120.2]]

# Haply board
CW  = 0
CCW = 1

haplyBoard          = Board
device              = Device
SimpleActuatorMech  = Mechanisms
pantograph          = Pantograph   

# File name in which results are stored
file_name = "data_storage.json"