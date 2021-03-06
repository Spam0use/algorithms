#!/usr/bin/env python

import pr3
import alg_cluster
import pr3viz
import random
import time
import pdb
import matplotlib.pyplot as plt

def gen_random_clusters(num_clusters):
    """
    <num_clusters> random clusters
    """
    out=[]
    for i in xrange(num_clusters):
        out.append(alg_cluster.Cluster(set([str(i)]),random.uniform(-1,1),random.uniform(-1,1),random.uniform(0.1,10),random.uniform(0.1,10)))
    return out
    
def time_closest_pairs(start=2,end=202,nstep=20,nreps=10):
    """
    q1
    """
    
    stp=(end-start)/min(end-start,nstep)
    rng=range(start,end,stp)
    lr=len(rng)
    out=[rng,[0]*lr,[0]*lr]
    #pdb.set_trace()
    for i in range(len(rng)):
        for j in xrange(nreps):
            clsts=gen_random_clusters(rng[i])
            st=time.time()
            pr3.slow_closest_pairs(clsts)
            elaps=time.time()-st
            out[1][i]+=elaps/nreps
            st=time.time()
            pr3.fast_closest_pair(clsts)
            elaps=time.time()-st
            out[2][i]+=elaps/nreps
    return out
    
def plotcp():
    """
    q4
    """
    tm=time_closest_pairs()
    plt.plot(tm[0],tm[1],label='slow_closest_pairs',color='red')
    plt.plot(tm[0],tm[2],label='fast_closest_pair',color='blue')
    plt.xlabel('n')
    plt.ylabel('avg time, s')
    plt.legend(loc='upper left')
    plt.title('execution time of closest pairs functions\n(desktop Python)')
    plt.show()
    plt.close()
        
        
def compute_distortion(cluster_list,nclust):
    """
    q7
    """
    cpy=[x[:] for x in cluster_list]
    #pdb.set_trace()
    km=pr3.kmeans_clustering(pr3viz.list2clust(cpy),nclust,5)
    kmdistn=sum([cl.cluster_error(cluster_list) for cl in km])
    cpy=[x[:] for x in cluster_list]
    hc=dist_hierarchical_clustering(pr3viz.list2clust(cpy),nclust)
    hcdistn=sum([cl.cluster_error(cluster_list) for cl in hc])
    return [kmdistn,hcdistn]
    
def dist_hierarchical_clustering(cluster_list, num_clusters,distrange):
    """
    q10 accessor fn
    """
    inputlist=[x[:] for x in cluster_list]
    #pdb.set_trace()
    cluster_list=pr3viz.list2clust(inputlist)
    ncl=len(cluster_list)
    out=[[0]*len(distrange),[0]*len(distrange)]
    outind=0
    while ncl>=num_clusters:
        clpr=pr3.fast_closest_pair(cluster_list)
        cluster_list[clpr[1]].merge_clusters(cluster_list[clpr[2]])
        del cluster_list[clpr[2]]
        if ncl in distrange:
            #pdb.set_trace()
            out[0][outind]=ncl
            out[1][outind]=sum([cl.cluster_error(inputlist) for cl in cluster_list])        
            outind+=1
        ncl-=1
    return out
    
def dist_clustering(cluster_list,cluster_range):
    """
    q10
    """    clusts=pr3viz.list2clust(cluster_list)
    clustout=dist_hierarchical_clustering(cluster_list,min(cluster_range),cluster_range)
    clustout.append([0]*len(clustout[0]))  #allocate array for kmeans
    for i in xrange(len(clustout[0])):
        k=clustout[0][i]
        km=pr3.kmeans_clustering(clusts,k,5)
        clustout[2][i]=sum([cl.cluster_error(cluster_list) for cl in km])
    return clustout
    
def q10(show=True):
    for county,url in {111:pr3viz.DATA_111_URL,290:pr3viz.DATA_290_URL,896:pr3viz.DATA_896_URL}.items():
        dat=pr3viz.load_data_table(url)
        cl=dist_clustering(dat,range(6,21))
        plt.plot(cl[0],cl[1],label='hierarchical')
        plt.plot(cl[0],cl[2],label='k-means')
        plt.xlabel('num clusters')
        plt.ylabel('distortion')
        plt.legend(loc='upper right')
        plt.title(str(county)+' county data set')
        if show:
            plt.show()
        else:
            plt.savefig('ap3q10_'+str(county)+'.png')
        plt.close()