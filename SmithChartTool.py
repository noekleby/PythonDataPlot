import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import numpy as np
from matplotlib.patches import Circle
'''
Plotting gammas read out from Advanced Design System in one (or optionally two) ASCII-file(s).

Plotting of contours for the Smith Chart is based on this solution: link.
'''

x_axis1 = [] # for the first ASCII-file
y_axis1 = []

x_axis2 = [] # for the second ASCII-file
y_axis2 = []
counter = 0

chartRadius = 1 # should always be 1 for this script
draw_labels = True # label the real and imaginary parts of the smith chart
ax = plt.gca() # axes to draw the chart on (get current axes)
#ax.set_title("Smith Chart Matching", va='top')

contour = []

userinput = input ("Read in your ASCII-file numero uno with gammas (filepath):")
with open(userinput, 'r') as f:
        next(f) # skip the first line
        for row in f:
            counter = counter + 1
            if counter%4 == 1: # only append every fourth line
                x_axis1.append(row[2:row.find(" ")])
                y_axis1.append(row[(row.find(" ")+3):row.find("\n")])
x_axis_int1 = list(map(float, x_axis1))
y_axis_int1 = list(map(float, y_axis1))

userinput2 = input ("ASCII-file number two if having (filepath/nofile):")
if userinput2 != "nofile":
    with open(userinput2, 'r') as f:
            counter = 0
            next(f)
            for row in f:
                counter = counter + 1
                if counter%4 == 1:
                    x_axis2.append(row[2:row.find(" ")])
                    y_axis2.append(row[(row.find(" ")+3):row.find("\n")])
    x_axis_int2 = list(map(float, x_axis2))
    y_axis_int2 = list(map(float, y_axis2))

# outer circle
outerCircle = Circle([0,0], chartRadius, ec='k', fc='None', visible=True)
ax.add_patch(outerCircle)

# draw x and y axis
ax.axhline(0, color='grey', lw=1, clip_path=outerCircle)
ax.axvline(1, color='k', clip_path=outerCircle)

rHeavyList = [0, 1]
xHeavyList = [1,-1] # Can these be removed and still maintain positions of the labels?

rLightList = np.array([ 0.2, 0.5, 1.0, 2.0, 5.0 ])
xLightList = np.array([ 0.2, 0.5, 1.0, 2.0 , 5.0, -0.2, -0.5, -1.0, -2.0, -5.0 ])

lightColor = dict(ec='grey', fc='none') # define color scheme with grey line color and none fill

# impedance/admittance circles
for r in rLightList:
    center = (r/(1.+r), 0)
    radius = 1./(1+r)
    contour.append(Circle(center, radius, **lightColor))
for x in xLightList:
    center = (1, 1./x)
    radius = 1./x
    contour.append(Circle(center, radius, **lightColor))

for r in rHeavyList:
    center = (r/(1.+r), 0)
    radius = 1./(1+r)
    contour.append(Circle(center, radius, **lightColor))
for x in xHeavyList:
    center = (1, 1./x)
    radius = 1./x
    contour.append(Circle(center, radius, **lightColor))

if draw_labels:
    #Clear axis
    ax.yaxis.set_ticks([])
    ax.xaxis.set_ticks([])
    for loc, spine in ax.spines.items():
        spine.set_color('none')
            
    ax.axis('image') # zoom properly

    #Annotate real part
    for value in rLightList:
        # Set radius of real part's label; offset slightly right
        # so label doesn't overlap chart's circles
        rho = (value - 1)/(value + 1) - 0.01
        ax.annotate(str(value), xy=(rho*radius, 0.01), xytext=(rho*radius, 0.01), ha = "right", va = "baseline")

    #Annotate imaginary part
    radialScaleFactor = 1.01 # Scale radius of label position by this factor. Making it >1 places the label
                                     # outside the Smith chart's circle

    for value in xLightList:
        #Transforms from complex to cartesian
        S = (1j*value - 1) / (1j*value + 1)
        S *= radius * radialScaleFactor
        rhox = S.real
        rhoy = S.imag

        # Choose alignment anchor point based on label's value
        if ((value == 1.0) or (value == -1.0)):
            halignstyle = "center"
        elif (rhox < 0.0):
            halignstyle = "right"
        else:
            halignstyle = "left"

        if (rhoy < 0):
            valignstyle = "top"
        else:
            valignstyle = "bottom"
        #Annotate value
        ax.annotate(str(value) + 'j', xy=(rhox, rhoy), xytext=(rhox, rhoy), ha = halignstyle, va = valignstyle)

    #Annotate 0 and inf
    ax.annotate('0.0', xy=(-1.02, 0), xytext=(-1.02, 0), ha = "right", va = "center")
    ax.annotate('$\infty$', xy=(radialScaleFactor, 0), xytext=(radialScaleFactor, 0), ha = "left", va = "center")


# loop though contours and draw them on the given axes
for currentContour in contour:
    cc=ax.add_patch(currentContour)
    cc.set_clip_path(outerCircle)

# Plotting gammas read out from the two files
for i in range(1,len(x_axis_int1)):
    angle = math.radians(y_axis_int1[i])
    x = x_axis_int1[i] * math.cos(angle) # Polar to cartesian
    y = x_axis_int1[i] * math.sin(angle)
    ax.annotate('*', color="blue", xy=(x, y))

if userinput2 != "nofile":
    for j in range(1,len(x_axis_int2)):
        angle = math.radians(y_axis_int2[j])
        x = x_axis_int2[j] * math.cos(angle)
        y = x_axis_int2[j] * math.sin(angle)
        ax.annotate('*', color="red", xy=(x, y))

plt.show() # Not to be used at the same time as Matplotlib2Tikz 
#from matplotlib2tikz import save as tikz_save
#tikz_save('plotOutput.tex') # For the purpose of Latex, matplotlib2tikz has to be installed
#^ Did not work properly though
