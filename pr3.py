#!/usr/bin/env python
"""
project 3, nearest neighbors & clusteirng

Student will implement four functions:

slow_closest_pairs(cluster_list)
fast_closest_pair(cluster_list) - implement fast_helper()
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a list of clusters in the plane
"""

import math
#import pickle
import random
#import pdb
#import os
#import sys
import alg_cluster

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function to compute Euclidean distance between two clusters
    in cluster_list with indices idx1 and idx2
    
    Returns tuple (dist, idx1, idx2) with idx1 < idx2 where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), idx1, idx2)


def slow_closest_pairs(cluster_list):
    """
    Compute the set of closest pairs of cluster in list of clusters
    using O(n^2) all pairs algorithm
    
    Returns the set of all tuples of the form (dist, idx1, idx2) 
    where the cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.   
    
    """
    clpr=[(float('inf'),-1,-1)]
    for cl1 in xrange(len(cluster_list)):
        for cl2 in xrange(cl1+1,len(cluster_list)):
            dtup=(cluster_list[cl1].distance(cluster_list[cl2]),cl1,cl2)
            if dtup[0]<clpr[0][0]:
                clpr=[dtup]
            elif dtup[0]==clpr[0][0]:
                clpr.append(dtup)
                
    return set(clpr)
    
def fast_closest_pair2(cluster_list):
    """
    -ive ctrl: run slow instead of fast
    """
    scp=slow_closest_pairs(cluster_list)
    return random.choice(list(scp))

def fast_helper(cluster_list, horiz_order, vert_order):
    """
    Divide and conquer method for computing distance between closest pair of points
    Running time is O(n * log(n))
    
    horiz_order and vert_order are lists of indices for clusters
    ordered horizontally and vertically
    
    Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
    cluster_list[idx1] and cluster_list[idx2]
    have the smallest distance dist of any pair of clusters

    """

    
    # base case
    if(len(horiz_order)<=3):
        choice= random.choice(list(slow_closest_pairs([cluster_list[ind] for ind in horiz_order])))
        return (choice[0],horiz_order[choice[1]],horiz_order[choice[2]])
      
    # divide
    half=int(math.ceil(len(horiz_order)/2.0))
    mid=0.5*(cluster_list[horiz_order[half-1]].horiz_center()+cluster_list[horiz_order[half]].horiz_center())  #horiz midpoint
    horizleft=horiz_order[:half]
    horizright=horiz_order[half:]
    vertleft=[ind for ind in vert_order if ind in horizleft]
    vertright=[ind for ind in vert_order if ind in horizright]
    dleft=fast_helper(cluster_list,horizleft,vertleft)
    dright=fast_helper(cluster_list,horizright,vertright)
    dmin=dleft if dleft[0]<dright[0] else dright
    
    # conquer
    
    # midset=[]
    # cont=[True,True]  #flag: continue search toward left & right of midpoint
    # inds=[len(horizleft)-1,0] #indices into horizleft & horizright
    # while cont[0] or cont[1]:  #search points around midpoint for those w/ dist<d
        # if abs(cluster_list[horizleft[inds[0]]].horiz_center()-mid)<dmin[0]:
            # midset.append(horizleft[inds[0]])
        # else:  
            # cont[0]=False
        # if abs(cluster_list[horizright[inds[1]]].horiz_center()-mid)<dmin[0]:
            # midset.append(horizright[inds[1]])
        # else:
            # cont[1]=False
        # if inds[0]>0:
            # inds[0]-=1
        # else:
            # cont[0]=False
        # if inds[1]<len(horizright)-1:
            # inds[1]+=1
        # else:
            # cont[1]=False
    # vertset=[ind for ind in vert_order if ind in midset]
    
    #2nd try
    horizset=[ind for ind in horiz_order if abs(cluster_list[ind].horiz_center()-mid)<dmin[0]]
    vertset=[ind for ind in vert_order if ind in horizset]
    
    #fallback, not optimal
    # vertset=vert_order  #shouldn't have to scan all items, just those near mid
    
    vertsetlen=len(vertset)
    for indu in xrange(vertsetlen-2):
        for indv in xrange(indu+1,min(indu+4,vertsetlen-1)):
            dmid=[cluster_list[vertset[indu]].distance(cluster_list[vertset[indv]]),vertset[indu],vertset[indv]]
            if dmid[0]<dmin[0]:
                #pdb.set_trace()
                dmin=tuple(dmid)
    return dmin  #dist, ind_i, ind_j    
    
def fast_closest_pair(cluster_list):
    """
    Compute a closest pair of clusters in cluster_list
    using O(n log(n)) divide and conquer algorithm
    
    Returns a tuple (distance, idx1, idx2) with idx1 < idx2 where
    cluster_list[idx1] and cluster_list[idx2]
    have the smallest distance dist of any pair of clusters
    """
                   
    # compute list of indices for the clusters ordered in the horizontal direction
    hcoord_and_index = [(cluster_list[idx].horiz_center(), idx) 
                        for idx in range(len(cluster_list))]    
    hcoord_and_index.sort()
    horiz_order = [hcoord_and_index[idx][1] for idx in range(len(hcoord_and_index))]
     
    # compute list of indices for the clusters ordered in vertical direction
    vcoord_and_index = [(cluster_list[idx].vert_center(), idx) 
                        for idx in range(len(cluster_list))]    
    vcoord_and_index.sort()
    vert_order = [vcoord_and_index[idx][1] for idx in range(len(vcoord_and_index))]

    # compute answer recursively
    answer = fast_helper(cluster_list, horiz_order, vert_order) 
    return (answer[0], min(answer[1:]), max(answer[1:]))

    

def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function mutates cluster_list
    
    Input: List of clusters, number of clusters
    Output: List of clusters whose length is num_clusters
    """
    
    ncl=len(cluster_list)
    while ncl>=num_clusters:
        clpr=fast_closest_pair(cluster_list)
        #pdb.set_trace()
        cluster_list[clpr[1]].merge_clusters(cluster_list[clpr[2]])
        del cluster_list[clpr[2]]
        ncl-=1
    return cluster_list



    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function mutates cluster_list
    
    Input: List of clusters, number of clusters, number of iterations
    Output: List of clusters whose length is num_clusters
    """
    
    # initialize k-means clusters to random points
    #means=random.choice(range(len(clust_list),num_clusters))    #initial clusters assigned to random data points
    
    #below only makes sense for grading:  initialize clusters deterministically to largest population counties
    workinglist=[itm.copy() for itm in cluster_list]
    workinglist=sorted(workinglist,key=lambda cls: cls.total_population(),reverse=True)
    means=[itm.copy() for itm in workinglist[:num_clusters] ]   #highest population items
    startidx=num_clusters   #for first pass, start assigning neighbors after initialized centers
    for dummy in xrange(num_iterations):
        membership=[-1]*len(workinglist)    #initialize cluster memberships
        for itmnum in xrange(startidx,len(workinglist)):
            itm=workinglist[itmnum]
            mindist=[float('inf'),-1]
            for idx,mean in enumerate(means):
                itmdist=mean.distance(itm)            
                if itmdist<mindist[0]:
                    mindist=[itmdist,idx]
            membership[itmnum]=mindist[1]
        for idx,itm in enumerate(membership):
            if itm>=0:
                means[itm].merge_clusters(workinglist[idx])
        clustering=[mean.copy() for mean in means] #copy clusters for posterity
        means=[alg_cluster.Cluster(set([]),itm.horiz_center(),itm.vert_center(),0,0.) for itm in means] #reset means to empty sets
        startidx=0  #prepare for next round
    return clustering


    





  
        