import math

x_axis1 = [] # for the first ASCII-file
y_axis1 = []

x_axis2 = [] # for the second ASCII-file
y_axis2 = []

counter = 0
'''
Convert gammas read out from Advanced Design System in one (or optionally two) ASCII-file(s)
to a .tex-file, giving a finished Smith Chart with coordinates in Latex.
'''
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

with open('inputmatch.tex', 'w') as fout:
    fout.write(r"\begin{tikzpicture}")
    fout.write(r"\begin{smithchart}[width=10cm]")
    for i in range(1,len(x_axis_int1)):
        angle = math.radians(y_axis_int1[i])
        x = x_axis_int1[i] * math.cos(angle) # Polar to cartesian
        y = x_axis_int1[i] * math.sin(angle)
        fout.write("\path[draw=blue] "+"("+str(x)+","+str(y)+")"+" circle (0.05cm);")
        
if userinput2 != "nofile":
    with open('inputmatch.tex', 'a') as fout:
        for j in range(1,len(x_axis_int2)):
            angle = math.radians(y_axis_int2[j])
            x = x_axis_int2[j] * math.cos(angle)
            y = x_axis_int2[j] * math.sin(angle)
            fout.write("\path[draw=red] "+"("+str(x)+","+str(y)+")"+" circle (0.05cm);")
        fout.write("\end{smithchart}")
        fout.write("\end{tikzpicture}")
else:
    with open('inputmatch.tex', 'a') as fout:
        fout.write("\end{smithchart}")
        fout.write("\end{tikzpicture}")
