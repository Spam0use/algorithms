#!/usr/bin/env python 

import pdb
import pr2
import ap1
import random
import numpy as np
import cPickle as pickle
import os
import matplotlib.pyplot as plt

def erugraph(nodes,prob):
    ''' 
    erdos-renyi random undirected graph of size 'nodes' 
    connected to each other node with probability 'prob' 
    '''
    graph={itm:set() for itm in range(nodes)}
    for tail in xrange(nodes):
        for head in xrange(nodes):
            rnd=random.random()
            if (tail != head) and (rnd<prob):    #no self loops
                graph[tail].add(head)
                graph[head].add(tail)
    return graph

def upagraph(n,m):
    ''' 
    preferential attachment random undirected graph of size n 
    seeded with size int(m) complete graph.  fractional m used in poisson process for selecting degree.
    '''
    #initialize to complete graph of first int(m) nodes (any loss of generality vs using random m nodes?)
    graph=ap1.make_complete_graph(int(m))
    deg=range(int(m))*int(m)
    for tail in xrange(int(m),n):
        graph[tail]=set([])
        samp=set([deg[i] for i in np.random.choice(a=len(deg),size=np.random.poisson(m),replace=True)]) 
        graph[tail]=samp
        for head in samp:
            graph[head].add(tail)
        deg.extend(samp)
        deg.extend([tail]*len(samp))
        #deg.append(tail)
    return graph
    
def edgecount(graph,undirected=True):
    """
    number of edges of  graph
    """
    edges=sum([len(x) for x in graph.values()])
    if undirected:
        edges=edges/2
    return edges
    
def random_order(ugraph):
    """ returns random order of nodes for compute_resilience"""
    nodes=ugraph.keys()
    attacks= np.random.choice(a=nodes,size=len(nodes),replace=False)
    return attacks
    
def random_attack(ugraph):
    """
    attack of random ordering of nodes in <ugraph>
    """
    attack=random_order(ugraph)
    return pr2.compute_resilience(ugraph,attack)

def resilience_plot_random(thresh=True,show=True):
    plt.plot(np.array(random_attack(net)),color='blue',label='empirical network, |V|=3112')
    plt.plot(np.array(random_attack(simneter)),color='red',label='erdos-renyi, p=0.0017, |V|=3040')
    plt.plot(np.array(random_attack(simnetupa)),color='green',label='preferential attachment, m=2.35, |V|=3069')
    if thresh:
        plt.plot(np.arange(1347,1,-1)*.75,color='gray',linestyle='--',label='resilience threshold')
    plt.legend(loc='upper right')
    plt.ylabel('largest connected component size')
    plt.xlabel('number nodes deleted')
    plt.title('resilience of empirical and simulated computer networks')
    if show:
		plt.show()
    else:
		plt.savefig('ap2f1.png')

def samplemaxdegree(graph):
	""" utility fn, return one node with maximum degree """
	degs=ap1.compute_in_degrees(graph)
	maxdeg=max(degs.values())
	maxnodes=[k for k,v in degs.items() if v==maxdeg]
	attack=np.random.choice(a=maxnodes,size=1)[0]
	return attack

def fast_targeted_order(ugraph):
    """ faster version of tergeted_order.  attacks graph by removing largest-degree node at each step"""
    degreeset={}
    for nod in ugraph.keys():
        degreeset[len(ugraph[nod])]=degreeset.get(len(ugraph[nod]),[])+[nod]
    print degreeset
    pdb.set_trace()
    attack=[]
    for k in xrange(max(degreeset.keys()),0,-1):
        if len(degreeset[k])>0:
            nod=np.random.choice(degreeset[k])
            neighs=ugraph[nod]
            degreeset[k].remove(nod)
            for neigh in neighs:
                neighdeg=[k for k,v in degreeset.items() if neigh in v][0]
                degreeset[neighdeg].remove(neigh)
                degreeset[neighdeg-1]=neigh
            attack.append(nod)
    return attack
