#!/usr/bin/env python 

import pdb
import pr2
import ap1
import random
import numpy as np
import pandas as pd
import cPickle as pickle
import os
import matplotlib.pyplot as plt
import time

def erugraph(nodes,prob):
    ''' 
    erdos-renyi random undirected graph of size 'nodes' 
    connected to each other node with probability 'prob' 
    '''
    graph={itm:set() for itm in range(nodes)}
    for tail in xrange(nodes):
        for head in xrange(tail+1,nodes):
            rnd=random.random()
            if (rnd<prob):   
                graph[tail].add(head)
                graph[head].add(tail)
    return graph

def upagraph(n,m,fractm='poisson'):
    ''' 
    preferential attachment random undirected graph of size n 
    seeded with size int(m) complete graph.  
    fractional m used in poisson process for selecting degree (fractm='poisson',
     otherwise choose between int(m) and int(m)+1 .
    '''
    #initialize to complete graph of first int(m) nodes (any loss of generality vs using random m nodes?)
    graph=ap1.make_complete_graph(int(m))
    deg=range(int(m))*int(m)
    for tail in xrange(int(m),n):
        graph[tail]=set([])
        if fractm=='poisson':
            samp=set([deg[i] for i in np.random.choice(a=len(deg),size=np.random.poisson(m),replace=True)]) 
        else:
            samp=set([deg[i] for i in np.random.choice(a=len(deg),size=int(m)+1 if np.random.random()<m-int(m) else int(m),replace=True)]) 
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
    
def resilience_plot_random(thresh=True,show=True):
    plt.plot(np.array(random_attack(net)),color='blue',label='empirical network, |V|=3112')
    plt.plot(np.array(random_attack(simneter)),color='red',label='erdos-renyi, p=0.0034, |V|=3056')
    plt.plot(np.array(random_attack(simnetupa)),color='green',label='preferential attachment, m=2.35, |V|=3157')
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

def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = pr2.copy_graph(ugraph)
    
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
    
                    
def fast_targeted_order(ugraph):
    """ putatively faster version of tergeted_order.  attacks graph by removing largest-degree node at each step"""
    graph=pr2.copy_graph(ugraph)
    n=len(graph)
    degreeset=[[] for i in range(n)]
    for nod in graph.keys():
        degreeset[len(graph[nod])]+=[nod]
    attack=[]
    for k in xrange(n-1,-1,-1):
        while len(degreeset[k])>0:
            node=np.random.choice(degreeset[k])
            degreeset[k].remove(node)
            neighbors=graph[node]
            for neigh in neighbors:
                d=[ind for ind,v in enumerate(degreeset) if neigh in v][0]
                degreeset[d].remove(neigh)
                degreeset[d-1]+=[neigh]
            attack.append(node)
            pr2.delete_node(graph,node)
    return attack            

def timetargeted():
    ns=range(10,1000,10)
    #graphs=[upagraph(n,5) for n in ns]
    df=pd.DataFrame(index=ns,columns=['targeted_order','fast_targeted_order'])
    for i in range(len(ns)):
        times=[]
        for j in range(5):
            gr=upagraph(ns[i],5)
            tm=time.time()
            devnull=targeted_order(gr)
            times.append(time.time()-tm)
        df.iloc[i,0]=np.mean(times)
        times=[]
        for j in range(5):
            gr=upagraph(ns[i],5)
            tm=time.time()
            devnull=fast_targeted_order(gr)
            times.append(time.time()-tm)
        df.iloc[i,1]=np.mean(times)
    return df
    
def plottimetargeted(df):
    plt.plot(df.index,df.iloc[:,0],label='targeted_order',color='red')
    plt.plot(df.index,df.iloc[:,1],label='fast_targeted_order',color='blue')
    plt.xlabel('n')
    plt.ylabel('avg time, s')
    plt.legend(loc='upper left')
    plt.title('execution time of targeted order functions\n(desktop Python)')
    plt.show()
    plt.close()
    
    plt.plot(df.index,df.iloc[:,0]**0.5,label='targeted_order',color='red')
    plt.plot(df.index,df.iloc[:,1]**0.5,label='fast_targeted_order',color='blue')
    plt.plot(df.index,(df.iloc[:,0]*7)**0.5,label='targeted_order * 7',color='red',linestyle='--')
    plt.xlabel('n')
    plt.ylabel('sqrt avg time, s')
    plt.legend(loc='upper left')
    plt.title('sqrt of execution time of targeted order functions')
    plt.show()
    plt.close()

def plottargetedresilience(show=True,thresh=True):
    plt.plot(pr2.compute_resilience(net,targeted_order(net)),label='empirical',color='blue')
    plt.plot(pr2.compute_resilience(simneter,targeted_order(simneter)),label='erdos-renyi, p=0.0034',color='red')
    plt.plot(pr2.compute_resilience(simnetupa,targeted_order(simnetupa)),label='preferenital attachment, m=2.35',color='green')
    plt.xlabel('number nodes deleted')
    plt.ylabel('largest connected component size')
    plt.title('resilience of empirical and simulated computer networks\n to targeted attacks')
    if thresh:
        plt.plot(np.arange(1347,1,-1)*.75,color='gray',linestyle='--',label='resilience threshold')
    plt.legend(loc='upper right')
    if show:
        plt.show()
    else:
        plt.savefig('ap2f3.png')
    plt.close()

# def fast_targeted_order(ugraph):
    # """ faster version of tergeted_order.  attacks graph by removing largest-degree node at each step"""
    # graph=pr2.copy_graph(ugraph)
    # degreeset={}
    # for nod in graph.keys():
        # degreeset[len(graph[nod])]=degreeset.get(len(graph[nod]),[])+[nod]
    # attack=[]
    # for k in xrange(max(degreeset.keys()),-1,-1):
        # while k in degreeset and len(degreeset[k])>0:
            # node=np.random.choice(degreeset[k])
            # attack.append(node)
            # neighbors=graph[node]
            # pr2.delete_node(graph,node)
            # degreeset[k].remove(node)
            # for neigh in neighbors:
                # neighdeg=[ind for ind,v in degreeset.items() if neigh in v][0]
                # degreeset[neighdeg].remove(neigh)
                # degreeset[neighdeg-1]=degreeset.get(neighdeg-1,[])+[neigh]
    # return attack          
    
#generate or load graphs
if(not os.path.isfile('nets.pkl')):
    net=pr2.load_graph(pr2.NETWORK_URL) #3112 edges
    simneter=erugraph(1347,.0034)    #3056 edges
    simnetupa=upagraph(1347,2.35)      #3157 edges
    pickle.dump([net,simneter,simnetupa],open('nets.pkl','wb'))
else:
    net,simneter,simnetupa=pickle.load(open('nets.pkl','rb'))
    
    