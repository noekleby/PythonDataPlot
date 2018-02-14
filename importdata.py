def importData():
        import matplotlib.pyplot as plt
        x_axis = []
        y_axis = []
        y_axis2 = []
        flag = 0
        counter = 0
        counter2 = 0
        userinput = input ("Hvilken noisy fil skal leses inn?")
        with open(userinput, 'r') as f:
                next(f)
                for row in f:
                        counter = counter + 1
                        if row.strip() == "":
                                flag = 1
                                break
                        x_axis.append(row[0:row.find("\t")])
                        y_axis.append(row[(row.find("\t")+1):row.find("\n")])
        x_axis_int = list(map(float, x_axis))
        y_axis_int = list(map(float, y_axis))
        plt.plot(x_axis_int,y_axis_int,'r')
        if flag == 1:
                with open(userinput, 'r') as fil:
                        for line in fil:
                                counter2 = counter2 + 1
                                if counter2 > counter+3 and line.strip() != "":
                                        y_axis2.append(line[(line.find("\t")+1):line.find("\n")])
                y_axis_int2 = list(map(float, y_axis2))
                plt.plot(x_axis_int,y_axis_int2,'b')
        plt.axis([1.3e9, 6e9, 0, 2])
        plt.grid(True)
        plt.ylabel('Noise')
        plt.xlabel('Frequency')
        plt.show()
importData()
