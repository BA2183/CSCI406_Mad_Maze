import networkx as net
# import matplotlib.pyplot as plt
# import string

# def drawRefurbishedGraph(graph, pos):
#     # size of plot
#     plt.figure(figsize=(10,10),dpi=100)
#     # set up position of graph items
        
#     # draw nodes
#     for node in graph.nodes():
#         net.draw_networkx_nodes(graph, pos,
#                                nodelist=list(graph.nodes()),
#                                node_size=250, node_color='red', alpha=0.9)
#         # print("drawn node:", node)
#     # draw edges
#     for edge in graph.edges:
#         net.draw_networkx_edges(graph, pos,
#                                edgelist=list(graph.edges()),
#                                width=3, alpha=0.9, edge_color='grey')
#         # print("drawn edge:", edge)
#     # draw network labels
#     labels={}
#     for node in graph.nodes():
#         # label according to PDF problem statement node labeling standard
#         if str(node) != 'win':
#             labels[node]=str(node[0]+1)+", "+str(node[1]+1)
#         else:
#             labels['win'] = 'win'
#     net.draw_networkx_labels(graph, pos, labels, font_size=5)
    
#     plt.axis('off')
#     plt.show()

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
    for i in range(n_edges):
        input_edge = input()
        if input_edge:
            from_node, to_node, edge_color = input_edge.split()
            in_maze.add_edge(int(from_node) - 1, int(to_node) - 1, color=edge_color)
            # print("add edge:", (from_node, to_node))

    # make state map
    state_graph = net.DiGraph()
    # win state
    win_state = 'win'
    state_graph.add_node(win_state)
    # add all states
    for lucky in range(len(color_map) + 1):
        for rocket in range(len(color_map) + 1):
            state_graph.add_node((rocket, lucky))
            # if state connect to winning
            if lucky == len(color_map) or rocket == len(color_map):
                state_graph.add_edge((rocket, lucky), win_state)
    
    # add edges between states
    for edge in in_maze.edges():
        for node in in_maze.nodes():
            # color match
            if in_maze.edges()[edge]['color'] == in_maze.nodes()[node]['color']: 
                    # add edges between either lucky colored room and rocket movement and vice versa
                    state_graph.add_edge((edge[0], node), (edge[1], node))
                    state_graph.add_edge((node, edge[0]), (node, edge[1]))
                    
    all_paths_str = []
    try:
        all_paths = net.all_shortest_paths(state_graph, starting_state, win_state)
    except net.NetworkXNoPath:
        print("NO PATH")
        return
    
    for path in all_paths:
        out_str = ""
        for step in range(len(path)):
            if step < len(path) - 2:
                # rocket moved
                if path[step][0] != path[step+1][0]:
                    out_str = out_str + "R" + str(path[step+1][0] + 1)
                
                # lucky moved
                if path[step][1] != path[step+1][1]:
                    out_str = out_str + "L" + str(path[step+1][1] + 1)
        all_paths_str.append(out_str)

    print(min(all_paths_str))

    # for node, neighbors in state_graph.adjacency():
    #     print("node:", node, "neighbors:", neighbors)
    # drawRefurbishedGraph(state_graph, net.fruchterman_reingold_layout(state_graph))
    
input_maze()