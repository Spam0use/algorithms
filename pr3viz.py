"""
Example code for creating and visualizing
cluster of county-based cancer risk data

Note that you must download the file
http://www.codeskulptor.org/#alg_clusters_matplotlib.py
to use the matplotlib version of this code
"""

# Flavor of Python - desktop or CodeSkulptor
DESKTOP = True

import math
import random
import urllib2
import pr3
import os
import cPickle as pickle
import pdb
import alg_cluster

# conditional imports
if DESKTOP:
    import alg_clusters_matplotlib
else:
    #import userXX_XXXXXXXX as alg_project3_solution   # CodeSkulptor project solution
    import alg_clusters_simplegui
    import codeskulptor
    codeskulptor.set_timeout(30)


###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"


def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]


############################################################
# Code to create sequential clustering
# Create alphabetical clusters for county data

def sequential_clustering(singleton_list, num_clusters):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters based on its ordering
    
    Note that method may return num_clusters or num_clusters + 1 final clusters
    """
    
    cluster_list = []
    cluster_idx = 0
    total_clusters = len(singleton_list)
    cluster_size = float(total_clusters)  / num_clusters
    
    for cluster_idx in range(len(singleton_list)):
        new_cluster = singleton_list[cluster_idx]
        if math.floor(cluster_idx / cluster_size) != \
           math.floor((cluster_idx - 1) / cluster_size):
            cluster_list.append(new_cluster)
        else:
            cluster_list[-1] = cluster_list[-1].merge_clusters(new_cluster)
            
    return cluster_list
                

#####################################################################
# Code to load cancer data, compute a clustering and 
# visualize the results


def run_example():
    """
    Load a data table, compute a list of clusters and 
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    data_table = load_data_table(DATA_111_URL)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
        
    # cluster_list = sequential_clustering(singleton_list, 15)
    # print "Displaying", len(cluster_list), "sequential clusters"

    # cluster_list = pr3.hierarchical_clustering(singleton_list, 9)
    # print "Displaying", len(cluster_list), "hierarchical clusters"

    cluster_list = pr3.kmeans_clustering(singleton_list, 9, 5)
    print "Displaying", len(cluster_list), "k-means clusters"

            
    # draw the clusters using matplotlib or simplegui
    if DESKTOP:
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)
    else:
        alg_clusters_simplegui.PlotClusters(data_table, cluster_list)
    
#run_example()

def list2clust(lst):
    """
    list of lists to list of clusters
    """
    out=[]
    for i in xrange(len(lst)):
        itm=lst[i]
        itm[0]=set([itm[0]])
        out.append(alg_cluster.Cluster(*itm))
    return out

if(not os.path.isfile('pr3.pkl')):
    test1L=[[111, 10., 10., 10, 1.],[112, 10., 11., 10, 2.], [113, 11., 10., 10, 1.], [114, 12., 12., 10, 1.]]
    test1=list2clust(test1L)
    data111L=load_data_table(DATA_111_URL)
    data111=list2clust(data111L)
    data896L=load_data_table(DATA_896_URL)
    data896=list2clust(data896L)
    data3108L=load_data_table(DATA_3108_URL)
    data3108=list2clust(data3108L)
    del test1L,data111L,data896L,data3108L
    pickle.dump([test1,data111,data896,data3108],open('pr3.pkl','wb'))
else:
    test1,data111,data896,data3108=pickle.load(open('pr3.pkl','rb'))

