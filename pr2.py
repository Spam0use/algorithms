#!/usr/bin/env python
"""
algorithmic thinking, Module 2
"""

# general imports
import urllib2
import random
import time
import math
#import matplotlib.pyplot as plt
from collections import deque

############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order
    


##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


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
    
EX_GRAPH1={0:set([1,4,5,3]),1:set([2,6,0,4]),2:set([3,1,5]),3:set([0,2]),4:set([1,0]),5:set([2,0]),6:set([1]),7:set([8]),8:set([7])}

def bfs_visited(ugraph,startnode):
    """
    return list of nodes in <ugraph> that are reachable from <startnode>
    """
    que=deque()
    visited=set([startnode])
    que.append(startnode)
    while(len(que)>0):
        idx=que.pop()
        for neigh in ugraph[idx]:
            if neigh not in visited:
                que.append(neigh)
                visited.add(neigh)
        # too-clever version, slower by 50%:
        # newnodes=[neigh for neigh in ugraph[idx] if neigh not in visited]
        # visited |= set(newnodes)
        # que.extend(newnodes)

    return visited
    
def cc_visited(ugraph):
    """
    given undirected graph <ugraph>, return connected components as sets of nodes
    """
    nodes=ugraph.keys()
    con=[]
    while len(nodes)>0:
        node=nodes.pop()
        reachable=bfs_visited(ugraph,node)
        con.append(reachable)
        nodes=[node for node in nodes if node not in reachable]
    return con
    
def largest_cc_size(ugraph):
    """
    given undirected graph <ugraph>, returns size of largest connected component
    """
    ccs=cc_visited(ugraph)
    return max([len(con) for con in ccs])
    
def largest_cc(ugraph):
	"""
	return largest connected component
	"""
	ccs=cc_visited(ugraph)
	ccsz=[len(itm) for itm in ccs]
	ccmx=ccsz.index(max(ccsz))
	return ccs[ccmx]

def compute_resilience(ugraph,attack_order):
	"""
	assess resiliance of undirected graph <ugraph> by measuring size of largest connected component
	"""
	graph=copy_graph(ugraph)
	con=largest_cc(graph)
	#print con
	out=[len(con)]
	for node in attack_order:
		#print node
		delete_node(graph,node)
		if node not in con:
			out.append(out[-1])		#node not in largest cc, no change
		else:
			con=largest_cc(graph)
			#print con
			out.append(len(con))
	return out
			
    
    





