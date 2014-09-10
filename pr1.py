''' exploring graph algorithms '''
#import numpy as np
#import pdb

EX_GRAPH0={0:set([1,2]),1:set([]),2:set([])}
EX_GRAPH1={0:set([1,4,5]),1:set([2,6]),2:set([3]),3:set([0]),4:set([1]),5:set([2]),6:set([])}
EX_GRAPH2={0:set([1,4,5]),1:set([2,6]),2:set([3,7]),3:set([7]),4:set([1]),5:set([2]),6:set([]),7:set([3]),8:set([1,2]),9:set([0,3,4,5,6,7])}

def make_complete_graph(num_nodes=3):
    ''' complete graph of size num_nodes returned as adjacency list
            in format {0:[1,2],...} indicating node 0 is connected to 1 & 2'''
    graph={}
    if num_nodes>0:
        for node in xrange(num_nodes):
            graph[node]=set([dummy_x for dummy_x in range(num_nodes) if dummy_x!=node])
    return graph
        
def compute_in_degrees(digraph):
    ''' compute in-degree of digraph represented as adjacency list. 
            returns dict with one item per node giving its in-
            degree'''
    #traverse graph, accumulate nodes of heads & tails of edges, resp:
    nodesin=[itm for subl in digraph.values() for itm in subl]
    nodesout=digraph.keys()
    nodes=list(set(nodesin+nodesout))  #deduplicate
    return {dummy_x:nodesin.count(dummy_x) for dummy_x in nodes}
    
    
def in_degree_distribution(digraph):
    ''' calculate in-degree distribution of digraph represented as 
            adjacency list.  returns    dict with one item in-degree 
            observed in graph, giving its count'''
    indegrees=compute_in_degrees(digraph)
    counts=indegrees.values()
    countset=list(set(counts))  #observed counts
    return {dummy_x:counts.count(dummy_x) for dummy_x in countset}
