#!/usr/bin/env python
import pr4
import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle
import os
import math
import random
import urllib2

# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"



###############################################
# provided code

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib2.urlopen(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict




def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urllib2.urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urllib2.urlopen(filename)

    # read in files as string
    words = word_file.read()

    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list

def q1():
    am=pr4.compute_alignment_matrix(dm,hs,pam,global_flag=False)
    al=pr4.compute_local_alignment(dm,hs,pam,am)
    return al
    
def pctaligned(a,b):
    """ percentage agreement between characters of a and b """
    ln=min(len(a),len(b))
    out=0
    for i in range(ln):
        out+=1 if a[i]==b[i] else 0
    return 100*out/float(ln)
    
def q2():
    al=q1()
    dmpax=al[1].replace('-','')
    hspax=al[2].replace('-','')
    dmal=pr4.compute_global_alignment(dmpax,pax,pam,pr4.compute_alignment_matrix(dmpax,pax,pam))
    hsal=pr4.compute_global_alignment(hspax,pax,pam,pr4.compute_alignment_matrix(hspax,pax,pam))
    return {'dm':pctaligned(dmal[1],dmal[2]),'hs':pctaligned(hsal[1],hsal[2])}
    
def nulldistribution(x,y,n):
    """ generate null distribution of alignment between x and y based on permutiona of y"""
    out={}
    yl=list(y)
    for i in range(n):
        random.shuffle(yl)
        ys=''.join(yl)
        #print ys
        s=pr4.compute_global_alignment(x,ys,pam,pr4.compute_alignment_matrix(x,ys,pam))[0]
        out[s]=out.get(s,0)+1
    return out
    
def q3(n=1000):
    distn=nulldistribution(dm,hs,n)
    scores=np.array(distn.keys())
    freq=np.array([distn[k] for k in scores])  #necessary?  freq=distn.values() guaranteed to give correct order?
    plt.bar(scores,freq/float(n))
    plt.xlabel('score')
    plt.ylabel('frequency')
    plt.title('distribution of alignment scores of shuffled sequences')
    plt.show()
    return [scores,freq]
    
def editdistance(x,y):
    alpha='abcdefghijklmnopqrstuvwxyz'
    am=pr4.build_scoring_matrix(alpha,2,1,0)
    al=pr4.compute_global_alignment(x,y,am,pr4.compute_alignment_matrix(x,y,am))
    out=len(x)+len(y)-al[0]
    return out
    
def checkspelling(word,dist,wordlist):
    out=[x for x in wordlist if editdistance(word,x)<=dist]
    return out
    
if(not os.path.isfile('ap4.pkl')):
    pam=read_scoring_matrix(PAM50_URL)
    hs=read_protein(HUMAN_EYELESS_URL)
    dm=read_protein(FRUITFLY_EYELESS_URL)
    pax=read_protein(CONSENSUS_PAX_URL)
    words=read_words(WORD_LIST_URL)
    pickle.dump([pam,hs,dm,pax,words],open('ap4.pkl','wb'))
else:
    pam,hs,dm,pax,words=pickle.load(open('ap4.pkl','rb'))