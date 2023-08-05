import markov_clustering as mc
import networkx as nx
import random
# number of nodes to use

Graph = nx.Graph()
    # 获取边列表edges_list
edges_list = []
line=['0:1','0:2','0:3','1:2','0:5','5:6','5:7','6:7']
for edge in line:
    edge_list = edge.split(':')
    edges_list.append((int(edge_list[0]), int(edge_list[1])))
# 为图增加边
Graph.add_edges_from(edges_list)
numnodes = 20

# generate random positions as a dictionary where the key is the node id and the value
# is a tuple containing 2D coordinates
positions = {i:(random.random() * 2 - 1, random.random() * 2 - 1) for i in range(numnodes)}
# print(positions)
# use networkx to generate the graph
network = nx.random_geometric_graph(numnodes, 0.3, pos=positions)
network=Graph
# then get the adjacency matrix (in sparse form)
matrix = nx.to_scipy_sparse_matrix(network)

result = mc.run_mcl(matrix,inflation=2)           # run MCL with default parameters
clusters = mc.get_clusters(result) 

# print(type(network))
# print(matrix)
# print(type(matrix))
print(clusters)