# import tkinter as tk

from tkinter import *
from tkinter import ttk
from tkinter import font
from PIL import Image,ImageTk
import tkinter.messagebox
import queue
import matplotlib.pyplot as plt

root = Tk()
root.title("AI Project")
root.geometry("1140x730+385+140")
# root.option_add( "*font", "AngsanaNew 14" )
root.option_add( "*font", "Times 14" )


mainframe_1 = Frame(root, bd=2, height=480, width=1140, relief = GROOVE)
# mainframe_1.pack()
mainframe_1.place(x=0, y=0)

mainframe_2 = Frame(root, bd=2, height=250, width=1140, relief = GROOVE)
# mainframe_2.pack()
mainframe_2.place(x=0, y=480)

# canvas = Canvas(root, width=300, height=5)
# canvas.pack()

photo = PhotoImage(file = '..\AI.PY\work3\miniproject_python\img.png')
label_img = Label(mainframe_1, image=photo)
# label_img.grid(row=0, column=0)
label_img.place(x=50, y=3)
# label_img.pack()

label_start = Label(root, text="จุดเริ่มต้น : ")
label_start.place(x=100, y=500)
# label_start.grid(row=1,column=0)
# label.configure(font = fonts)
# label_start.pack()

dropdown_var1 = StringVar()
# dropdown_var2 = StringVar()
dropdown_1 = ttk.Combobox(root, textvariable=dropdown_var1,width=20)
# dropdown_2 = ttk.Combobox(root, textvariable=dropdown_var2,width=20)
dropdown_1['values'] = ('ต้นไม้1', 'ต้นไม้2', 'ต้นไม้3', 'ต้นไม้4')
# dropdown_2['values'] = ('ต้นไม้1', 'ต้นไม้2', 'ต้นไม้3', 'ต้นไม้4')
# dropdown_1.grid(row=1,column=1)
dropdown_1.place(x=155, y=500)
# label_to = Label(root, text="จุดสิ้นสุด : ")
# label_to.place(x=420, y=500)
# label_to.grid(row=1,column=3)
# label_to.pack()
# dropdown_2.grid(row=1,column=4)
# dropdown_2.place(x=473, y=500)

# getting heuristics from file
def getHeuristics():
    heuristics = {}
    f = open("..\AI.PY\work3\miniproject_python\heuristics.txt")
    for i in f.readlines():
        node_heuristic_val = i.split()
        heuristics[node_heuristic_val[0]] = int(node_heuristic_val[1])

    return heuristics


# getting cities location from file
def getCity():
    city = {}
    citiesCode = {}
    f = open("..\AI.PY\work3\miniproject_python\cities.txt")
    j = 1
    for i in f.readlines():
        node_city_val = i.split()
        city[node_city_val[0]] = [int(node_city_val[1]), int(node_city_val[2])]

        citiesCode[j] = node_city_val[0]
        j += 1

    return city, citiesCode


# creating cities graph from file
def createGraph():
    graph = {}
    file = open("..\AI.PY\work3\miniproject_python\citiesGraph.txt")
    for i in file.readlines():
        node_val = i.split()

        if node_val[0] in graph and node_val[1] in graph:
            c = graph.get(node_val[0])
            c.append([node_val[1], node_val[2]])
            graph.update({node_val[0]: c})

            c = graph.get(node_val[1])
            c.append([node_val[0], node_val[2]])
            graph.update({node_val[1]: c})

        elif node_val[0] in graph:
            c = graph.get(node_val[0])
            c.append([node_val[1], node_val[2]])
            graph.update({node_val[0]: c})

            graph[node_val[1]] = [[node_val[0], node_val[2]]]

        elif node_val[1] in graph:
            c = graph.get(node_val[1])
            c.append([node_val[0], node_val[2]])
            graph.update({node_val[1]: c})

            graph[node_val[0]] = [[node_val[1], node_val[2]]]

        else:
            graph[node_val[0]] = [[node_val[1], node_val[2]]]
            graph[node_val[1]] = [[node_val[0], node_val[2]]]

    return graph


# Greedy Best First Search Algorithm
def GBFS(startNode, heuristics, graph, goalNode="Bucharest"):
    priorityQueue = queue.PriorityQueue()
    priorityQueue.put((heuristics[startNode], startNode))

    path = []

    while priorityQueue.empty() == False:
        current = priorityQueue.get()[1]
        path.append(current)

        if current == goalNode:
            break

        priorityQueue = queue.PriorityQueue()

        for i in graph[current]:
            if i[0] not in path:
                priorityQueue.put((heuristics[i[0]], i[0]))

    return path

# drawing map of answer
def drawMap(city, gbfs, graph):
    for i, j in city.items():
        plt.plot(j[0], j[1], "ro")
        plt.annotate(i, (j[0] + 5, j[1]))

        for k in graph[i]:
            n = city[k[0]]
            plt.plot([j[0], n[0]], [j[1], n[1]], "gray")

    for i in range(len(gbfs)):
        try:
            first = city[gbfs[i]]
            secend = city[gbfs[i + 1]]

            plt.plot([first[0], secend[0]], [first[1], secend[1]], "green")
        except:
            continue

    plt.errorbar(1, 1, label="GBFS", color="green")
    plt.legend(loc="lower left")
    plt.show()

# running the program
def main():
    heuristic = getHeuristics()
    graph = createGraph()
    city, citiesCode = getCity()

    for i, j in citiesCode.items():
        print(i, j)

    while True:
        inputCode = int(input("Please enter your desired city's number (0 for exit): "))

        if inputCode == 0:
            break

        cityName = citiesCode[inputCode]

        gbfs = GBFS(cityName, heuristic, graph)
        print("GBFS => ", gbfs)
        drawMap(city, gbfs, graph)


def perform_action():

        showresult_1 = Label(text = "จุดเริ่มต้น : " + dropdown_var1.get())
        showresult_1.place(x=340, y=560)
        
        showresult_2 = Label(text = "จุดสิ้นสุด : " + "Bucharest")
        showresult_2.place(x=340, y=600)

        # showresult_1.grid(row=2,column=0)
        # showresult_2.grid(row=3,column=0)



action_button = Button(root, text="SUBMIT", command=perform_action, font="Arial 15", bg='green', fg='white')
# action_button.grid(row=1,column=5)
action_button.place(x=740, y=492)

# action_button.pack()

# result_label = Label(root, text="",font=("Arial", 25))
# result_label.pack()

# main()
root.mainloop()
