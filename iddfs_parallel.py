# Python program to print DFS traversal from a given
# given graph
from collections import defaultdict
import pickle
import pandas as pd
import csv
from joblib import Parallel, delayed

# load_data = pickle.load(open("quotes_02_clustered_sample.dat", "rb" ))
load_data = pickle.load(open("cluster_membership.dat", "rb" ))
node_dictionary = []
edge_table = []

# This class represents a directed graph using adjacency
# list representation
class Graph:

    def __init__(self, vertices):

        # No. of vertices
        self.V = vertices

        # default dictionary to store graph
        self.graph = defaultdict(list)

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    # A function to perform a Depth-Limited search
    # from given source 'src'
    def DLS(self, src, target, maxDepth):

        if src == target : return True

        # If reached the maximum depth, stop recursing.
        if maxDepth <= 0 : return False

        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[src]:
                if(self.DLS(i,target,maxDepth-1)):
                    return True
        return False

    # IDDFS to search if target is reachable from v.
    # It uses recursive DLS()
    def IDDFS(self, src, target, maxDepth):

        # Repeatedly depth-limit search till the
        # maximum depth
        for i in range(maxDepth):
            if (self.DLS(src, target, i)):
                return True
        return False

def first(iterable, default=None):
    for item in iterable:
        return item
    return default

g = Graph (len(load_data));

node_dict = pd.read_csv("node_dictionary.csv")
node_dict_length = len(node_dict.values)

with open('node_dictionary.csv') as csvfile:
    reader = csv.DictReader(csvfile)

    for x in range(0, node_dict_length):
        node_dictionary.append("dummy")

    for row in reader:
        source = int(row['Index'])
        link = row['P']
        node_dictionary[source] = link

with open('edge_table_numeric.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        source = int(row['Source'])
        target = int(row['Target'])
        g.addEdge(source, target)
        edge = {}
        edge['Source'] = source
        edge['Target'] = target
        edge_table.append(edge)

# print(node_dictionary)
# print(edge_table)

maxDepth = 50
count_true = 0
count_false = 0

count_reachable = []
for i in range(0, len(load_data)):
    count_reachable.append(0)

def check_reachable(tuple_of_index):
    i = tuple_of_index[0]
    j = tuple_of_index[1]
    k = tuple_of_index[2]

    if g.IDDFS(cluster[j]['index'],cluster[k]['index'], maxDepth) == True:
        print(str(cluster[j]['index']) + " -> " + str(cluster[k]['index']) + " is reachable.")
        count_reachable[i] += 1

for i, cluster in enumerate(load_data):
    print("Cluster",i)
    num_data = len(cluster)
    list_for_checking = []
    for j in range(0,num_data-1):
        for k in range(j+1,num_data):
            list_for_checking.append((i,j,k))

    n_jobs = -1
    Parallel(n_jobs=n_jobs)(delayed(check_reachable)(tup) for tup in list_for_checking)

for i, cluster in enumerate(load_data):
    reachable = count_reachable[i]
    unreachable = len(cluster) - count_reachable[i]
    print("Cluster", i)
    print("Reachable:", reachable)
    print("Unreachable:", unreachable)
    print("Percentage:", reachable/len(cluster)*100, "%")

# for x in range(0, node_dict_length-1):
#     for y in range(x+1, node_dict_length):
#         if g.IDDFS(x, y, maxDepth) == True:
#             print(str(x) + " -> " + str(y) + " is reachable.")
#             source_link = node_dictionary[x]
#             target_link = node_dictionary[y]

#             source_data = first(data for data in load_data if data.get('P') == source_link)
#             print(source_data)

#             if [data for data in load_data if data.get('P') == target_link] == True:
#                 target_data = first(data for data in load_data if data.get('P') == target_link)
#                 print(target_data)
#                 if (source_data['C'] == target_data['C']):
#                     print(str(x) + " -> " + str(y) + " is in the SAME cluster.")
#                     count_true += 1
#                 else:
#                     print(str(x) + " -> " + str(y) + " is NOT in the SAME cluster.")
#                     count_false += 1
#             else:
#                 print("Node " + str(y) + " is NOT found.")
#         else:
#             print(str(x) + " -> " + str(y) + " is NOT reachable.")
#         print("\n")

# if g.IDDFS(src, target, maxDepth) == True:
#     print ("Target is reachable from source " +
#         "within max depth")
# else :
#     print ("Target is NOT reachable from source " +
#         "within max depth")
