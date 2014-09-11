#!/usr/bin/env python 

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
    seeded with size m complete graph 
    '''
    #initialize to complete graph of first m nodes (any loss of generality vs using random m nodes?)
    graph=ap1.make_complete_graph(m)
    deg=range(m)*m
    for tail in xrange(m,n):
        graph[tail]=set([])
        samp=set([deg[i] for i in np.random.choice(a=len(deg),size=m,replace=True)]) 
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
    
def random_attack(ugraph):
    """
    attack of random ordering of nodes in <ugraph>
    """
    nodes=ugraph.keys()
    attacks= np.random.choice(a=nodes,size=len(nodes),replace=False)
    return pr2.compute_resilience(ugraph,attacks)
    
def resilience_plot_random(thresh=True):
    plt.plot(np.array(random_attack(net)),color='blue',label='empirical network')
    plt.plot(np.array(random_attack(simneter)),color='red',label='erdos-renyi, p=0.0017')
    plt.plot(np.array(random_attack(simnetupa)),color='green',label='preferential attachment, m=2')
    if thresh:
        plt.plot(np.arange(1347,1,-1)*.75,color='gray',linestyle='--',label='resilience threshold')
    plt.legend(loc='upper right')
    plt.ylabel('largest connected component size')
    plt.xlabel('number nodes deleted')
    plt.title('resilience of empirical and simulated computer networks')
    plt.show()
    
#generate or load graphs
if(not os.path.isfile('nets.pkl')):
    net=pr2.load_graph(pr2.NETWORK_URL) #3112 edges
    simneter=erugraph(1347,.0017)    #3092 edges
    simnetupa=upagraph(1347,2)      #2683 edges
    pickle.dump([net,simneter,simnetupa],open('nets.pkl','wb'))
else:
    net,simneter,simnetupa=pickle.load(open('nets.pkl','rb'))
    
