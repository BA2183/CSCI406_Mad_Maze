import networkx as net
import matplotlib.pyplot as plt

def input_maze():
    # read in number of nodes and edges
    n_nodes, n_edges = input().split()
    n_nodes = int(n_nodes)
    n_edges = int(n_edges)

    # read in color map
    color_map = input().split()

    # read in Lucky and Rocket starting node
    rocket_start, lucky_start = input().split()
    rocket_start = int(rocket_start)
    lucky_start  = int(lucky_start)
    starting_state = (rocket_start, lucky_start)

    # make maze
    in_maze = net.MultiDiGraph()

    # add nodes
    for node_num in range(len(color_map)):
        in_maze.add_node(node_num + 1, color=color_map[node_num])
    in_maze.add_node(len(color_map) + 1, color="W")

    # read edges
    for i in range(n_edges):
        input_edge = input()
        # make sure for empty input
        if input_edge:
            from_node, to_node, edge_color = input_edge.split()
            in_maze.add_edge(int(from_node), int(to_node), color=edge_color)

    # make state map
    state_graph = net.DiGraph()

    # win state
    win_state = 'win'
    state_graph.add_node(win_state)

    # add all states
    for lucky in range(len(color_map) + 1):
        for rocket in range(len(color_map) + 1):
            state_graph.add_node((rocket + 1, lucky + 1))

            # if state connect to winning
            if lucky == len(color_map) or rocket == len(color_map):
                state_graph.add_edge((rocket + 1, lucky + 1), win_state)
    
    # add edges between states
    for edge in in_maze.edges(keys=True):
        for node in in_maze.nodes():
            # color match
            if in_maze.edges(keys=True)[(edge)]['color'] == in_maze.nodes()[node]['color']: 
                    # add edges between either lucky colored room and rocket movement and vice versa
                    state_graph.add_edge((edge[0], node), (edge[1], node))
                    state_graph.add_edge((node, edge[0]), (node, edge[1]))
                    
    all_paths_str = []
    try:
        all_paths = net.all_shortest_paths(state_graph, starting_state, win_state)

        for path in all_paths:
            out_str = ""
            for step in range(len(path)):
                if step < len(path) - 2:
                    # rocket moved
                    if path[step][0] != path[step+1][0]:
                        out_str = out_str + "R" + str(path[step+1][0])
                    
                    # lucky moved
                    if path[step][1] != path[step+1][1]:
                        out_str = out_str + "L" + str(path[step+1][1])
            all_paths_str.append(out_str)

        print(min(all_paths_str))
    except net.NetworkXNoPath:
        print("NO PATH")
        return
    
    all_paths = net.all_shortest_paths(state_graph, starting_state, win_state)
    return state_graph, all_paths, all_paths_str, starting_state, win_state
    
logic_maze, all_paths, all_paths_str, start_state, win_state = input_maze()
all_paths_list = [path for path in all_paths]
short_path_color = all_paths_list[all_paths_str.index(min(all_paths_str))]

coloring_node = {}
for node in logic_maze.nodes():
    if node in short_path_color:
        coloring_node[node] = 'yellow'
    else:
        coloring_node[node] = 'white'

coloring_node[win_state] = 'green'
coloring_node[start_state] = 'red'

coloring_edge = {}
for edge in logic_maze.edges():
    if edge[0] in short_path_color and edge[1] in short_path_color:
        coloring_edge[edge] = 'blue'
    else:
        coloring_edge[edge] = 'black'

color_map_node = [coloring_node[node] for node in logic_maze.nodes()]
color_map_edge = [coloring_edge[edge] for edge in logic_maze.edges()]
layout = net.kamada_kawai_layout(logic_maze)
net.draw(logic_maze, pos=layout, node_color=color_map_node, edge_color=color_map_edge, with_labels=True, node_size=120, font_size=5)
plt.show()
