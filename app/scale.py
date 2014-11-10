import numpy as np


def scale(x, y, screen_width, screen_height):
    
    # get the farthest point (x_lim, y_lim)
    x_lim = max(abs(min(x)), abs(max(x)))
    y_lim = max(abs(min(y)), abs(max(y)))
    
    # add a little padding for good measure
    box = max(x_lim, y_lim) * (1.2)
    
    # get the largest radius possible without overshooting screen
    # TO DO: Figure out how to use browser window size sted screen size
    d = min(screen_width/2, screen_height/2) * (1 - 0.1)

    # get ratio "largest radius possible : smallest box that still fits all points"
    # TO DO: Ask B about this -- not sure
    delta = d/box
    
    # scale x and y according to ratio, then shift location to center of screen
    x_norm = (x*delta + screen_width/2) 
    y_norm = (y*delta + screen_height/2)
    
    return zip(x_norm, y_norm)

if __name__ == '__main__':

    # TO DO: Figure out number of points this should be
	npoints = 100000

    # TO DO: I think this should just be an increment (0.1)
	t = (np.random.rand(npoints) -0.5) * 100
	
    # ASK ABOUT THIS: I think these should not be arrays--should be set numbers.
    # ALSO: Get these values from algorithm.py
    a = (np.random.rand(npoints) -0.5) * 100
	b = (np.random.rand(npoints) -0.5) * 100
	h = (np.random.rand(npoints) -0.5) * 100

    # TO DO: get this from Javascript or Processing.js
	screen_width = 1200
	screen_height = 750

    # TO DO: Get equation for epitrochoid (outer ring)
    # x =
    # y = 

    # Equation for hypotrochoids (interior rings)
	x  =  ((a-b) * np.cos(t)) + (h * np.cos(((a-b)/b) * t))  
	y  =  ((a-b) * np.sin(t)) - (h * np.sin(((a-b)/b) * t))

	points = scale(x, y, screen_width, screen_height)
