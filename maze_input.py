import networkx as net
import matplotlib.pyplot as plt
import string

# def drawRefurbishedGraph(graph, pos):
#     # size of plot
#     plt.figure(figsize=(10,10),dpi=100)
#     # set up position of graph items
        
#     # draw nodes
#     for node in graph.nodes():
#         net.draw_networkx_nodes(graph, pos,
#                                nodelist=list(graph.nodes()),
#                                node_size=250, node_color='red', alpha=0.9)
#         print("drawn node:", node)
#     # draw edges
#     for edge in graph.edges:
#         net.draw_networkx_edges(graph, pos,
#                                edgelist=list(graph.edges()),
#                                width=3, alpha=0.9, edge_color='grey')
#         print("drawn edge:", edge)
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

    for edge in in_maze.edges():
        for rocket in range(len(color_map)+1):
            for lucky in range(len(color_map)+1):
                if rocket == edge[0] and in_maze.edges()[edge]['color'] == in_maze.nodes()[lucky]['color']:
                    state_graph.add_node((rocket, lucky))
                    state_graph.add_node((edge[1], lucky))
                    state_graph.add_edge((rocket, lucky), (edge[1], lucky))
                elif rocket == len(color_map):
                    state_graph.add_edge((rocket, lucky), win_state)
                else:
                    state_graph.add_node((rocket, lucky))
                
                if lucky == edge[0] and in_maze.edges()[edge]['color'] == in_maze.nodes()[rocket]['color']:
                    state_graph.add_node((rocket, lucky))
                    state_graph.add_node((rocket, edge[1]))
                    state_graph.add_edge((rocket, lucky), (rocket, edge[1]))
                elif lucky == len(color_map):
                    state_graph.add_edge((rocket, lucky), win_state)
                else:
                    state_graph.add_node((rocket, lucky))

    # def check_lucky(current_state, next_node):
    #     if in_maze.edges()[(current_state[0], next_node)]['color'] == in_maze.nodes()[current_state[1]]['color']:
    #         # move lucky if same color
    #         next_state = (next_node, current_state[1])
    #         # add to graph
    #         # print("add state:", next_state)
    #         state_graph.add_node(next_state)
    #         # check in matrix
    #         if state_matrix[next_state[0]][next_state[1]] == -1:
    #             # print("add edge between", current_state, "and", next_state)
    #             state_graph.add_edge(current_state, next_state)
    #         next_state_check(next_state)

    # def check_rocket(current_state, next_node):
    #     if in_maze.edges()[(current_state[1], next_node)]['color'] == in_maze.nodes()[current_state[0]]['color']:
    #         # move rocket if same color
    #         next_state = (current_state[0], next_node)
    #         # add to graph
    #         # print("add state:", next_state)
    #         state_graph.add_node(next_state)
    #         # check in matrix
    #         if state_matrix[next_state[0]][next_state[1]] == -1:
    #             # print("add edge between", current_state, "and", next_state)
    #             state_graph.add_edge(current_state, next_state)
    #         next_state_check(next_state)

    # def next_state_check(current_state):
    #     if state_matrix[current_state[0]][current_state[1]] == -1:
    #         state_matrix[current_state[0]][current_state[1]] = current_state
    #         for next_lucky_move in list(in_maze.adj.items())[current_state[0]][1]:
    #             check_lucky(current_state, next_lucky_move)
    #         for next_rocket_move in list(in_maze.adj.items())[current_state[1]][1]:
    #             check_rocket(current_state, next_rocket_move)
    #     elif current_state[0] == len(color_map) or current_state[1] == len(color_map):
    #             state_graph.add_edge(current_state, win_state)

    # current_state = starting_state
    # next_state_check(current_state)

    # correct_order = [starting_state] + [to_node for from_node, to_node in net.bfs_edges(state_graph, starting_state)]
    # out_str = ""
    # for idx in range(len(correct_order)):
    #     if idx+1 < len(correct_order):
    #         if correct_order[idx][0] != correct_order[idx+1][0]:
    #             out_str = out_str + 'R' + str(correct_order[idx+1][0]+1)
    #             # print("rocket move to", correct_order[idx+1][0] + 1)
            
    #         if correct_order[idx][1] != correct_order[idx+1][1]:
    #             out_str = out_str + 'L' + str(correct_order[idx+1][0]+1)
    #             # print("lucky move to", correct_order[idx+1][1] + 1)
    # print(out_str)
    # drawRefurbishedGraph(state_graph, net.fruchterman_reingold_layout(state_graph))
    
input_maze()