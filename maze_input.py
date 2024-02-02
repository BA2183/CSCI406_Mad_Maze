import networkx as net
import matplotlib.pyplot as plt
import string

def drawRefurbishedGraph(graph, pos):
    # size of plot
    plt.figure(figsize=(10,10),dpi=100)
    # set up position of graph items
        
    # draw nodes
    for node in graph.nodes():
        net.draw_networkx_nodes(graph, pos,
                               nodelist=list(graph.nodes()),
                               node_size=250, node_color='red', alpha=0.9)
        # print("drawn node:", node)
    # draw edges
    for edge in graph.edges:
        net.draw_networkx_edges(graph, pos,
                               edgelist=list(graph.edges()),
                               width=3, alpha=0.9, edge_color='grey')
        # print("drawn edge:", edge)
    # draw network labels
    labels={}
    for node in graph.nodes():
        # label according to PDF problem statement node labeling standard
        if str(node) != 'win':
            labels[node]=str(node[0]+1)+", "+str(node[1]+1)
        else:
            labels['win'] = 'win'
    net.draw_networkx_labels(graph, pos, labels, font_size=5)
    
    plt.axis('off')
    plt.show()

def input_maze():
    # read in number of nodes and edges
    n_nodes, n_edges = input().split()
    n_nodes = int(n_nodes)
    n_edges = int(n_edges)

    # read in color map
    color_map = input().split()

    # read in Lucky and Rocket starting node
    rocket_start, lucky_start = input().split()
    rocket_start = int(rocket_start) - 1
    lucky_start  = int(lucky_start)  - 1
    starting_state = (rocket_start, lucky_start)

    # make maze
    in_maze = net.DiGraph()

    # add nodes
    for node_num in range(len(color_map)):
        in_maze.add_node(node_num, color=color_map[node_num])
        # print("add node:", node_num)
    in_maze.add_node(len(color_map), color='W')

    # read edges
    for i in range(int(n_edges)):
        from_node, to_node, edge_color = input().split()
        in_maze.add_edge(int(from_node) - 1, int(to_node) - 1, color=edge_color)
        # print("add edge:", (from_node, to_node))

    # make state map
    state_graph = net.DiGraph()
    win_state = 'win'
    state_graph.add_node(win_state)

    # keep track if a state already found
    state_matrix = [[-1 for j in range(len(color_map) + 1)] for i in range(len(color_map) + 1)]

    # check the edge
    for edge in in_maze.edges():
        # check possible rocket location
        for rocket in range(len(color_map)+1):
            # check possible lucky location
            for lucky in range(len(color_map)+1):
                # if rocket location is at a from node of an edge and color of the edge match lucky, rocket move
                if rocket == edge[0] and in_maze.edges()[edge]['color'] == in_maze.nodes()[lucky]['color']:
                    # add the current state
                    state_graph.add_node((rocket, lucky))
                    # add the next state
                    state_graph.add_node((edge[1], lucky))
                    # connect the state
                    state_graph.add_edge((rocket, lucky), (edge[1], lucky))
                elif rocket == len(color_map):
                    # if rocket location is at the final node, connect to win state
                    state_graph.add_edge((rocket, lucky), win_state)
                else:
                    # no connection, add the current state
                    state_graph.add_node((rocket, lucky))
                
                # same thing, but it is for lucky
                if lucky == edge[0] and in_maze.edges()[edge]['color'] == in_maze.nodes()[rocket]['color']:
                    state_graph.add_node((rocket, lucky))
                    state_graph.add_node((rocket, edge[1]))
                    state_graph.add_edge((rocket, lucky), (rocket, edge[1]))
                elif lucky == len(color_map):
                    state_graph.add_edge((rocket, lucky), win_state)
                else:
                    state_graph.add_node((rocket, lucky))

    # drawRefurbishedGraph(state_graph, net.fruchterman_reingold_layout(state_graph))
    
input_maze()