"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import urllib2
import cPickle as pickle
import os.path
import random
import numpy as np

# Set timeout for CodeSkulptor if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph


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
    nodesin=[itm for sublst in digraph.values() for itm in sublst]
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

def erdigraph(nodes,prob):
    ''' erdos-renyi random graph of size 'nodes' connected to each other node with probability 'prob' '''
    graph={itm:set() for itm in range(nodes)}
    for tail in xrange(nodes):
        for head in xrange(nodes):
            rnd=random.random()
            if (tail != head) and (rnd<prob):    #no self loops
                graph[tail].add(head)
    return graph
    
def dpadigraph(n,m):
    ''' preferential attachment random graph of size n seeded with size m complete graph '''
    #initialize to complete graph of first m nodes (any loss of generality vs using random m nodes?)
    graph=make_complete_graph(m)
    indeg=range(m)*m
    for node in xrange(m,n):
        graph[node]=set([])
        #samp=set(np.random.choice(a=len(indeg),size=m,replace=True))
        #by profiling, 'choice' call rate limiting, version below ~100x faster than naive above
        samp=set([indeg[i] for i in np.random.choice(a=len(indeg),size=m,replace=True)]) 
        graph[node]=samp
        indeg.extend(samp)
        indeg.append(node)
    return graph
        

if(not os.path.isfile('cid.pkl')):
    citation_graph = load_graph(CITATION_URL)
    cid=in_degree_distribution(citation_graph)
    pickle.dump(cid,open('cid.pkl','wb'))
else:
    cid=pickle.load(open('cid.pkl','rb'))



