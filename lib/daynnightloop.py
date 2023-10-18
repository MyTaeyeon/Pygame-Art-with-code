import pygame
import math
import numpy as np

pygame.init()

def filter(array,t = 0):

	twave = math.sin(t*0.01+1)

	for x in np.nditer(array[0],op_flags=['readwrite'],flags=['external_loop']):
		x[...]= (x-35+twave*45)/(1.3-twave*0.3)

	for x in np.nditer(array[1],op_flags=['readwrite'],flags=['external_loop']):
		x[...] = (x-35+twave*44)/(1.3-twave*0.3)

	for x in np.nditer(array[2],op_flags=['readwrite'],flags=['external_loop']):
		x[...] = (x-25+twave*25)/(1.3-twave*0.3)