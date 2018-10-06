#!/usr/bin/env python2
import sys
from Queue import PriorityQueue
import math

cityList=[] # for the latitude and longitude
roadList=[] # for the road segments

for cityrow in open('city-gps.txt', 'r'):
    cityname, lat, long = cityrow.split()
    cityList.append((str(cityname),float(lat),float(long)))

# if the speed isn't mentioned then its taken as the mean of all speed limits
for road in open('road-segments.txt', 'r'):
    if len(road.split())==5:
        startCity,endCity,distance,speedLimit,highwayName=road.split()        
        roadList.append((str(startCity),str(endCity),float(distance),float(speedLimit),str(highwayName)))            
    else:
        t=road.split()
        startCity, endCity, distance, speedLimit, highwayName=t[0], t[1], t[2], float(30) , t[3]
        roadList.append((str(startCity), str(endCity), float(distance), float(speedLimit), str(highwayName)))

#Successor for all the functions
# beenCities keeps track of all the cities visited so that the program doesn't get stuck in a loop
def successors(succ,beenCities):
    cities = []
    
    for success1 in roadList:       
        if (success1[0] == succ):
            if success1[3]!=0: #for speed =0, we have ignored the road.
                cities.append([success1[1], succ,success1[2],float(success1[2])/success1[3],1])
        elif success1[1] == succ:
            if success1[3]!=0:
                cities.append([success1[0], succ,success1[2],float(success1[2])/success1[3],1])
    #Remove visited cities            
    for success2 in beenCities:
        for success3 in cities:
            if (success2 == success3[0]):
                cities.remove(success3)
                
    for city in cities:
        beenCities.append(city[0])
    return cities
    
# heuristics of distance, time and segments
def heuristic(succ,psucc):
    succ_coord = []
    for success in cityList:
        if success[0]==succ:
            succ_coord.append(success[1])
            succ_coord.append(success[2])
    if len(succ_coord)==0:
        #[euclid_dist,flight_time] = heuristic(psucc,'xyz')
        euclid_dist = 0     
        flight_time = 0  
        segments = 0
    else:
        euclid_dist = math.sqrt(math.pow(succ_coord[0]-dest_coord[0],2)+math.pow(succ_coord[1]-dest_coord[1],2))       
        flight_time = float(euclid_dist)/max_speed  
        segments = int(euclid_dist/max_distance)

    return [euclid_dist,flight_time,segments]  
    
def is_goal(state):
    if state==destination:
        return True
    else:
        return False

#BFS and DFS with all cost functions
def solve(ini_state):
    beenCities=['Mumbai']
    fringe = [[ini_state,ini_state,0,0,0]]
    while len(fringe) > 0:
        if routingalgorithm == 'bfs' or routingalgorithm == 'uniform' :
            [state, route_so_far,dist_from_source,time_from_source, no_of_segments] = fringe.pop(0)
        else:
            [state, route_so_far, dist_from_source,time_from_source,no_of_segments] = fringe.pop()
        for [succ,move,dist,time, segment] in successors( state,beenCities ):

            if is_goal(succ):
                A = [route_so_far + " " +succ]
                newList=[]
                for items in A:
                    newList.extend(items.split())
                if costfunction == 'segments' and (routingalgorithm =='bfs' or routingalgorithm =='uniform'):
                    print 'yes',
                else:
                    print 'no',
                print dist_from_source+dist,
                print round(time_from_source+time,3),
                for values in newList:
                    print values,
                return True
            fringe.append([succ, route_so_far + " " + succ, dist_from_source+dist,time_from_source+time,no_of_segments+segment])
        
    return False

#Uniform with cost=distance
def solve_uniform1(ini_state):
    beenCities=['Mumbai']
    fringe=PriorityQueue()
    fringe.put((0,[ini_state,ini_state,0,0,0]))
    while not(fringe.empty()):
        (p,[state, route_so_far,dist_from_source,time_from_source, no_of_segments]) = fringe.get()
        for [succ, move,dist,time,segment] in successors( state,beenCities ):
            if is_goal(succ):

                A = [route_so_far+" " +succ]
                newList=[]
                for items in A:
                    newList.extend(items.split())
                if costfunction == 'distance':
                    print 'yes',
                else:
                    print 'no',
                print dist_from_source+dist,
                print round(time_from_source+time,3),
                for values in newList:
                    print values,
                return True

            fringe.put((p + dist, [succ, route_so_far + " " + succ,dist_from_source+dist,time_from_source+time,no_of_segments+segment]))    
    return False

#Uniform with cost = time    
def solve_uniform2(ini_state):
    beenCities=['Mumbai']
    fringe=PriorityQueue()
    fringe.put((0,[ini_state, ini_state,0,0,0]))
    while not(fringe.empty()):
        (p,[state, route_so_far,dist_from_source,time_from_source, no_of_segments]) = fringe.get()
        for [succ, move,dist,time,segment] in successors( state,beenCities ):
            if is_goal(succ):

                A = [route_so_far + " " +succ]
                newList=[]
                for items in A:
                    newList.extend(items.split())
                if costfunction == 'time':
                    print 'yes',
                else:
                    print 'no',
                print dist_from_source+dist,
                print round(time_from_source+time,3),
                for values in newList:
                    print values,
                return True

            fringe.put((p + time, [succ, route_so_far + " " + succ,dist_from_source+dist,time_from_source+time,no_of_segments+segment]))    
    return False

# Astar for Distance Heuristic
# Our heuristic is the euclidian distance admissable as it can't possibly overestimate the distance between any two cities in united states. We have neglected with safety the curvature of earth
def solve_Astar1(ini_state):
    beenCities=['Mumbai']
    fringe=PriorityQueue()
    fringe.put((0,[ini_state, ini_state,0,early_dist,0]))
    while not(fringe.empty()):
        (p,[state, route_so_far,dist_from_source,time_from_source, no_of_segments]) = fringe.get()
        for [succ, move,dist,time,segment] in successors( state,beenCities ):
            if is_goal(succ):
                A = [route_so_far + " " +succ]
                newList=[]
                for items in A:
                    newList.extend(items.split())
                if costfunction == 'distance':
                    print 'yes',
                else:
                    print 'no',
                print dist_from_source+dist,
                print round(time_from_source+time,3),
                for values in newList:
                    print values,
                return True
            [h_dist,h_time, h_segments]=heuristic(succ,state)
            if h_dist ==0:
                fringe.put((dist + p, [succ, route_so_far + " " + succ,dist_from_source+dist,time_from_source+time, no_of_segments+segment]))    
            else:
                fringe.put((dist_from_source+ dist + h_dist, [succ, route_so_far + " " + succ,dist_from_source+dist,time_from_source+time,no_of_segments+segment]))    
    return False  

# Astar for Time Heuristic
#Our heuristic is Euclidian diatance by maximum speed in the list which will give us the lowest time, and thus cant be overestimated.
def solve_Astar2(ini_state):
    beenCities=['Mumbai']
    fringe=PriorityQueue()
    fringe.put((0,[ini_state, ini_state,0,early_dist,0]))
    while not(fringe.empty()):
        (p,[state, route_so_far,dist_from_source,time_from_source, no_of_segments]) = fringe.get()
        for [succ, move,dist,time,segment] in successors( state,beenCities ):
            if is_goal(succ):
                A = [route_so_far + " " +succ]
                newList=[]
                for items in A:
                    newList.extend(items.split())
                if costfunction == 'time':
                    print 'yes',
                else:
                    print 'no',
                print dist_from_source+dist,
                print round(time_from_source+time,3),
                for values in newList:
                    print values,
                return True
                
            [h_dist,h_time,h_segments]=heuristic(succ,state)
            if h_dist ==0:
                fringe.put((time + p, [succ, route_so_far + " " + succ,dist_from_source+dist,time_from_source+time,no_of_segments+segment]))    
            else:
                fringe.put((time_from_source+ time + h_time, [succ, route_so_far + " " + succ,dist_from_source+dist,time_from_source+time,no_of_segments+segment]))    
    return False  

# Astar for Segment Heuristic
# Our heuristic is Euclidean distance by the length of the largest segment, which will give us the least number of segments between any two cities and thus can't be overestimated
def solve_Astar3(ini_state):
    beenCities=['Mumbai']
    fringe=PriorityQueue()
    fringe.put((0,[ini_state, ini_state,0,early_dist,0]))
    while not(fringe.empty()):
        (p,[state, route_so_far,dist_from_source,time_from_source, no_of_segments]) = fringe.get()
        for [succ, move,dist,time,segment] in successors( state,beenCities ):
            
            if is_goal(succ):
                A = [route_so_far + " " +succ]
                newList=[]
                for items in A:
                    newList.extend(items.split())
                if costfunction == 'segments':
                    print 'yes',
                else:
                    print 'no',
                print dist_from_source+dist,
                print round(time_from_source+time,3),
                for values in newList:
                    print values,
                return True
            [h_dist,h_time,h_segments]=heuristic(succ,state)
            if h_dist ==0:
                fringe.put((1 + p, [succ, route_so_far + " " + succ,dist_from_source+dist,time_from_source+time,no_of_segments+segment]))    
            else:
                fringe.put((no_of_segments+segment + h_segments, [succ, route_so_far + " " + succ,dist_from_source+dist,time_from_source+time,no_of_segments+segment]))    
    return False  

#
   

def solve_ids(ini_state):
    i=1
    while i<len(cityList):
        fringe = [[ini_state,ini_state,0,0,0]]
        beenCities = ["Mumbai"]
    
        while len(fringe) > 0:

            [state, route_so_far,dist_from_source,time_from_source,no_of_segments] = fringe.pop()
            if (no_of_segments)<=seg*i:
                for [succ,move,dist,time,segment] in successors( state, beenCities ):
            
                    if is_goal(succ):
                        
                        A = [route_so_far+ " " + succ]
                        newList=[]
                        for items in A:
                            newList.extend(items.split())
                        print 'no',
                        print dist_from_source+dist,
                        print round(time_from_source+time,3),
                        for values in newList:
                            print values,
                        return True
                
                    fringe.append([succ, route_so_far + " " + succ, dist_from_source+dist,time_from_source+time,no_of_segments + segment  ])
        i+=1
    return False


seg=20 #step size for IDS

#Taking inputs
source=(sys.argv[1])
destination=(sys.argv[2])
routingalgorithm=(sys.argv[3])
costfunction=(sys.argv[4])
#source='Bloomington,_Indiana'
#destination='Chicago,_Illinois'
#routingalgorithm='astar'
#costfunction='time'
ini_state = source

dest_coord = []
source_coord = []
for city in cityList:
    if city[0] == destination:
        dest_coord.append(city[1])
        dest_coord.append(city[2])
for city in cityList:
    if city[0] == source:
        source_coord.append(city[1])
        source_coord.append(city[2])
        
        
#eucledian distance between source and destination
early_dist = math.sqrt(math.pow(source_coord[0] - dest_coord[0], 2) + math.pow(source_coord[1] - dest_coord[1], 2))
speed = []
distance = []
for road in roadList:
    speed.append(road[3])
    # print(road[2])
    distance.append(road[2])
#maximum speed limit in US
max_speed = max(speed)
#maximum length of any road in US
max_distance = max(distance)
#solve_Astar1(ini_state)
if routingalgorithm=='bfs':
    solve(ini_state)
elif routingalgorithm=='uniform' and costfunction=='distance':
    solve_uniform1(ini_state)
elif routingalgorithm=='uniform' and costfunction=='time':
    solve_uniform2(ini_state)
elif routingalgorithm=='uniform' and costfunction=='segments':
    solve(ini_state) #We'll be basically solving bfs as it is equivalent to uniform with cost = segments
elif routingalgorithm=='dfs' :
    solve(ini_state)
elif routingalgorithm=='ids' :
    solve_ids(ini_state)
elif routingalgorithm=='astar' and costfunction=='time':
    solve_Astar2(ini_state)
elif routingalgorithm=='astar' and costfunction=='distance':
    solve_Astar1(ini_state)
elif routingalgorithm=='astar' and costfunction=='segments':
    solve_Astar3(ini_state)










