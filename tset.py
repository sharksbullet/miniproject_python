from tkinter import *
from tkinter import ttk
from tkinter import font
import tkinter.messagebox
import queue
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# getting heuristics from file
def getHeuristics():
    heuristics = {}
    f = open("..\py\work3\\miniproject_python\heuristics.txt")
    for i in f.readlines():
        node_heuristic_val = i.split()
        heuristics[node_heuristic_val[0]] = int(node_heuristic_val[1])
    
    return heuristics


# getting cities location from file
def getCity():
    city = {}
    citiesCode = {}
    f = open("..\py\work3\\miniproject_python\cities.txt")
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
    file = open("..\py\work3\miniproject_python\citiesGraph.txt")
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
            plt.plot([j[0], n[0]], [j[1], n[1]], "Gainsboro")

    for i in range(len(gbfs)):
        try:
            first = city[gbfs[i]]
            secend = city[gbfs[i + 1]]

            plt.plot([first[0], secend[0]], [first[1], secend[1]], "DarkGreen")
        except:
            continue


#GUI and running program
def root():
    
    root = Tk()
    root.title("AI Project")
    root.geometry("1140x730+220+30")

    heuristic = getHeuristics()
    graph = createGraph()
    city, citiesCode = getCity()
    fig,ax = plt.subplots()

    
    frame = Frame(root)
    

    frame.pack()

    frame_label_1 = LabelFrame(frame, border=0)
    frame_label_1.grid(row=0, column=0, padx=20, pady=20)

    for widget in frame_label_1.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    frame_label_2 = LabelFrame(frame, border=0)
    frame_label_2.grid(row=1, column=0, padx=20, pady=10)

    dropdown_var = StringVar()
    dropdown = ttk.Combobox(frame_label_2, textvariable=dropdown_var, values=['Select City', *city], width=53, state="readonly")
    dropdown.current(0)
    dropdown.grid(row=0,column=0)
    
    def on_click():
        dropdown_1 = dropdown_var.get()
        cityName = dropdown_1
        if dropdown_var.get() != 'Select City': 
            frame_label_3 = LabelFrame(frame_label_2, border=0)
            frame_label_3.grid(row=1, column=0, padx=20, pady=10)
            
            label_start_txt = Label(frame_label_3, text="Starting in : " + dropdown_1, bg="white", width=47)
            label_start_txt.grid(row=1,column=0)

            label_end_txt = Label(frame_label_3, text = "Ending in : " + "Bucharest", bg="white", width=47)
            label_end_txt.grid(row=2,column=0)

            gbfs = GBFS(cityName, heuristic, graph)
            label_print_gbfs = Label(frame_label_3, text=[*gbfs], bg="white", width=47)
            label_print_gbfs.grid(row=3,column=0)

            drawMap(city, gbfs, graph)
            canvas =FigureCanvasTkAgg(fig,master=frame)
            canvas.get_tk_widget().grid(row=0,column=0)

            for widget in frame_label_3.winfo_children():
                widget.grid_configure(padx=5, pady=5)

    btn_1 = Button(frame_label_2, text="SUBMIT", command=on_click, width=10)
    btn_1.grid(row=0,column=1)

    for widget in frame_label_2.winfo_children():
        widget.grid_configure(padx=10, pady=5)
    
    root.mainloop()


if __name__ == '__main__':
    root()