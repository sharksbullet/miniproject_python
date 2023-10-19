from tkinter import *
from tkinter import ttk
from tkinter import font
import queue
import matplotlib.pyplot as plt

# getting heuristics from file
def getHeuristics():
    heuristics = {}
    f = open("..\miniproject_python\Treeheuristics.txt")
    for i in f.readlines():
        node_heuristic_val = i.split()
        heuristics[node_heuristic_val[0]] = int(node_heuristic_val[1])
    
    return heuristics


# getting cities location from file
def gettree():
    tree = {}
    treeCode = {}
    f = open("..\miniproject_python\Trees.txt")
    j = 1
    for i in f.readlines():
        node_tree_val = i.split()
        tree[node_tree_val[0]] = [int(node_tree_val[1]), int(node_tree_val[2])]

        treeCode[j] = node_tree_val[0]
        j += 1

    return tree, treeCode


# creating cities graph from file
def createGraph():
    graph = {}
    file = open("..\miniproject_python\TreesGraph.txt")
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
def GBFS(startNode, heuristics, graph, goalNode="Opium"):
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
def drawMap(tree, gbfs, graph):
    for i, j in tree.items():
        plt.plot(j[0], j[1], "ro")
        plt.annotate(i, (j[0] + 5, j[1]))

        for k in graph[i]:
            n = tree[k[0]]
            plt.plot([j[0], n[0]], [j[1], n[1]], "Gainsboro")

    for i in range(len(gbfs)):
        try:
            first = tree[gbfs[i]]
            secend = tree[gbfs[i + 1]]

            plt.plot([first[0], secend[0]], [first[1], secend[1]], "DarkGreen")
        except:
            continue
    
    plt.show()


#GUI and running program
def root():
    
    root = Tk()
    root.title("Greedy Best First Search")
    root.state('zoomed')
    root.geometry("1160x730+220+30")
    root.configure(bg='#CECECE')
    
    heuristic = getHeuristics()
    graph = createGraph()
    tree, treeCode = gettree()

    frame = Frame(root, bg="#CECECE")
    frame.pack()

    frame_label_1 = LabelFrame(frame, bg="#3D3E3A", border=0)
    frame_label_1.grid(row=0, column=0, padx=10, pady=10)

    photo = PhotoImage(file = '..\miniproject_python\pathmap.png')
    label_img = Label(frame_label_1, image=photo, width=1127, height=546)
    label_img.grid(row=0, column=0)

    for widget in frame_label_1.winfo_children():
        widget.grid_configure(padx=1, pady=1)

    frame_label_2 = LabelFrame(frame, border=0, bg="#CECECE")
    frame_label_2.grid(row=1, column=0, padx=20, pady=10)

    frame_label_24 = LabelFrame(frame_label_2, border=0)
    frame_label_24.grid(row=0, column=0, padx=20, pady=10)

    dropdown_var = StringVar()
    dropdown = ttk.Combobox(frame_label_2, textvariable=dropdown_var, values=['Select Tree', *tree], width=53, state="readonly")
    dropdown.current(0)
    dropdown.grid(row=0,column=0)
    
    def on_click():
        dropdown_1 = dropdown_var.get()
        treeName = dropdown_1
        if dropdown_var.get() != 'Select Tree' :
            frame_label_3 = LabelFrame(frame, border=0, bg="#CECECE")
            frame_label_3.grid(row=2, column=0, padx=10, pady=10)
            
            label_start_txt = Label(frame_label_3, text="Starting in : " + dropdown_1, anchor="w",justify="left", bg="White", width=62)
            label_start_txt.grid(row=1,column=0) 

            label_end_txt = Label(frame_label_3, text = "Ending in : " + "Opium", anchor="w",justify="left", bg="White", width=62)
            label_end_txt.grid(row=2,column=0)

            gbfs = GBFS(treeName, heuristic, graph)
            label_print_gbfs = Label(frame_label_3, text=['Output', '-->', *gbfs], anchor="w",justify="left", bg="White", width=62)
            label_print_gbfs.grid(row=3,column=0)

            print("Tree Select => ", dropdown_1)
            print("GBFS => ", gbfs)

            for widget in frame_label_3.winfo_children():
                widget.grid_configure(padx=5, pady=5)

            plt.rcParams['figure.figsize'] = [10, 5]
            drawMap(tree, gbfs, graph)


    frame_label_25 = LabelFrame(frame_label_2, border=0)
    frame_label_25.grid(row=0, column=1, padx=20, pady=10)

    btn_1 = Button(frame_label_25, text="SUBMIT", command=on_click, width=10, bg="#01F9C6")
    btn_1.grid(row=0,column=0)

    for widget in frame_label_2.winfo_children():
        widget.grid_configure(padx=10, pady=5)
    
    root.mainloop()


if __name__ == '__main__':
    root()