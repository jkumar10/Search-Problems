#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 01 11:16:35 2018

@author: MAHESH
"""
""" We have two ways of generating groups
1st- Uniform search(which we have implemented
2nd- random search where we create new states by randomly adding a specific number
of groups to a state to create new successors. If the number of groups added is equal to the number of combinations
which could be added to a state, then it is uniform search
On line 142 if the number of random groups created is equal to number of groups
which could be added without replacement, then its uniform search,
else it is random search.
Random seach won't guarantee cost minimization as uniform search does. )"""

import sys
from Queue import PriorityQueue
import math
import random 
import itertools as it
inputfile = sys.argv[1]
k = int(sys.argv[2])
m = int(sys.argv[3])
n = int(sys.argv[4])    

studentchoice = {}
#    studentchoice = []

inputList = []
names = []
preferlist = []
nonpreferlist = []
with open(inputfile, "r") as myfile:
    f = myfile.read().splitlines()
    for line in f:
        studentID, size, prefer, notPrefer = line.split(" ")
        preferlist = prefer.split(",")
        nonpreferlist = notPrefer.split(",")
        if len(preferlist)==1:
            preferlist.append('_')
        my_dict = {
            "student":studentID,
                "gsize": size,
                "plist": preferlist,
                "nplist": nonpreferlist
            
        };

        inputList.append(my_dict)       
        studentchoice[studentID] = [size, preferlist, notPrefer]
        names.append(studentID)# list of all the students
# all the possible combinations of size,1,2,3 of the students
comb = list(it.combinations(names,1)) + list(it.combinations(names,2)) + list(it.combinations(names,3))



    
def solve(ini_state):    
    fringe=PriorityQueue()
    fringe.put((0,ini_state))
    while not(fringe.empty()):
        (p,state) = fringe.get()        
        for succ in successors(state):
            if is_goal(succ):
                for lines in succ:
                    lines=(' '.join(str(v) for v in lines))
                    print lines
                print(cost(succ))
                return True
            fringe.put((cost(succ), succ))    
    return False
    
def cost(state):
    global k
    temp_list = []
    for succ in state:
        temp_list+=list(succ)
    cost = len(state)*k 
   
# for groups of different size   
    for groups in state:
        l2 = list(groups)        
        for i in range(len(l2)):
            for success in inputList:                           
                if success['student']==l2[i]:                     
                    if success['gsize']==str(len(l2)):
                        cost = cost
                    else:
                        cost +=1 

# for groups of people not grouped with people they wanted                        
        for i in range(len(l2)):
            for success in inputList:                
                if success['student'] == l2[i]:
                    temp1 = success['plist']                    
                    for j in range(len(temp1)):
                        for success1 in inputList:
                            if success1['student']==temp1[j]:
                                if success1['plist'][0]!=l2[i] and success1['plist'][1]!=l2[i] :
                                    cost+=n

# for groups of students grouped with people who they did'nt want to work with                                    
        for i in range(len(l2)):
            for success in inputList:
                if success['student'] == groups[i]:
                    temp3 = success['nplist']
                    for j in range(len(temp3)):                                
                        for person in l2:
                            if person==temp3[j]:
                                cost+=m
                               
    return cost



def successors(state1):
    taken = []#a list of all the students of the state
    new_comb = list(it.combinations(names,1)) + list(it.combinations(names,2)) + list(it.combinations(names,3))

    for i in range(len(state1)):
        taken = taken +list(state1[i])

    temp = []
    for success in new_comb:
        rem = 0
        for i in range(len(success)):
            for j in range(len(taken)):
                if success[i]==taken[j]:
                    rem = 1 # to tag the groups having students of the state
        if rem == 1:
            temp.append(success)

    for success in temp: # to create a combination such that no group in it has the students of the present state
        new_comb.remove(success)
              
    successor = []

    # generating a list of all the groups of updated combinations
    r = random.sample(new_comb,len(new_comb))
    
    for succ in r:
        state2 = state1 + [succ] # creating new states
        successor.append(state2)
        
    return successor

def is_goal(state1):
    temp2 = []
    for i in range(len(state1)):
        temp = list(state1[i])
        temp2 += temp
    
    if len(temp2)!=len(names):
        return False
            
    return True
                           
            
                    
initial_state = []
solve(initial_state)
                
