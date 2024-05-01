#A free lunch, algorithms to turn a dollar into a million
#By Liam Purcell
#video describing the code - https://youtu.be/j3l87ks1mrA

#I apologize for some of the informality in this project, I was taking a lot of notes for myself in the #s, some are real though processes others are me losing it

import networkx as nx 
import matplotlib.pyplot as plt
import math
import random as r


# n currencies
# r_ij describes rate from one to another
# r_ii = 1
# all r_ij >= 0
# theoretically there exists a path from i to i that makes more than you began with
# steps
    # making a directed graph ex.
        # usd to gbp = 1.5 so gbp to usd = .67 more nodes ofc
    #from node 1, check all other options list as the most advantageous to 2,3,4,
        # move on to node 2 check all options, if most advantageous update 3,4,5,...
            # continue until all paths are explored
            # in my research of how to do all of this, I learned this is a dijkstra algorithm
            # idk how to code it though so :(

# make an algorithm that finds the shortest path from a to b, from currency one to two utilizing ^^
# you'd never believe what networkx has as a default, a dijkstra algorithm

#proof of concept for n nodes (currencies) here n = 5

def test():
    g = nx.DiGraph() #making a graph that goes both ways allowing for trading to and from one currency to another
    g.add_edge(1,2,weight=3)
    g.add_edge(2,3,weight=1)
    g.add_edge(1,4,weight=1)
    g.add_edge(4,3,weight=9)
    g.add_edge(4,5,weight=8)
    g.add_edge(3,5,weight=1)

    nx.draw_spring(g, with_labels=True, )
    plt.show()

    print(nx.dijkstra_path(g,1,5,weight='weight'))   #returns shortest path same as below
    print(nx.shortest_path(g, 1, 5, weight = 'weight'))  #prints 1,2,3,5 which is expected as it is the path with the lowest sum of weights
    #   functionally I don't see how these vary, but I know that dijkstra checks all paths effectively as I know how that one works, shortest path is magic to me
    ### UPDATE FROM A LATER DAY I now know that Bellman-Ford also wouldve found the shortest path, but works with negative weights too, but that isnt important here


#I can't find data, so I'm going to show that the algorithm works for a random # of currencies w random rates in both ways

def BestPath():   #takes two integer values and shows the most advantageous path from one to another
    numOfCurrencies = r.randint(10,15) #ideally the 15 is bigger but my laptop will explode
    print("there are ", numOfCurrencies, "currencies")
    global G
    G = nx.DiGraph()
    for i in range(int(numOfCurrencies)):
        for j in range(int(numOfCurrencies)):
            if j > i:
                iToj = int(r.uniform(.1, 5.0) * 100) / 100
                iToj = math.log(iToj)     #dijkstra does addition not multiplication, logarithm makes that possible
                iToj = (int(iToj * 100)) / 100
                G.add_edge(int(i)+1,int(j)+1, weight = iToj)
                # was there for checking  ------------------  print(int(i)+1, "to", int(j)+1, "weight is", iToj)
    bestPath()


def bestPath():
    nx.draw_spring(G, with_labels=True, )
    plt.show()

    print(nx.johnson(G ,weight='weight'))


###print(nx.dijkstra_path_length(G ,int(start), int(end) ,weight='weight'))

# apply above with real data, can't find decent usuable data to and from many currencies only to and from USD
# so here is that, it could easily be
## this can be ignored to --------------  this doesn't work and i can't figure out why or what I was thinking

def USD():
    text = open(file = 'rates.csv')
    lines = text.readlines()
    g = nx.DiGraph()
    g.add_node("USD")
    
    for line in lines[1:]:
        line = line.strip().split(',')
        country = line[1]
        rate = line[2]
        g.add_edge("USD", country, weight = float(rate))
        g.add_edge(country, "USD", weight = 1/float(rate))
        print(country) #just to see whats being read 
    nx.draw_spring(g, with_labels=True)
    plt.show()

## ------------------------------------------------------------------


#actually answering the question
# Im just copying and pasting the question so I dont have to keep going back and forth              ###
###  Give an efficient algorithm for the following problem: Given a set of exchange rates ri,j ,    ###
###  and two currencies s and t, find the most advantageous sequence of currency exchanges for      ###
###  converting currency s into currency t. Toward this goal, you should represent the currencies   ###
###  and rates by a graph whose edge lengths are real numbers.                                      ###

#coding dijkstras algo, if wanted I'll speak to you tomorrow
#problems I encountered and the solutions, I didnt use logs at first, not actually representative of what we wanted
#log(n) n<1 = -number, dijkstra cant handle that, use bellman ford
#I cannot gaurentee there wont be negative cycles w random numbers, bellman ford breaks
#GOOGLE LED ME TO JOHNSON'S ALGO and all is good

import heapq

def dijk(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))

    return distances

graph = {
    'A': {'B': 5, 'C': 2},
    'B': {'A': 5, 'C': 1, 'D': 3},
    'C': {'A': 2, 'B': 1, 'D': 1},
    'D': {'B': 3, 'C': 1, 'E': 2},
    'E': {'D': 2}
}

start_node = 'A'
distances = dijk(graph, start_node)

print("Shortest distances from node", start_node + ":")
for node, distance in distances.items():
    print("To node", node + ":", distance)


## finds the shortest path from a node to all other nodes in the graph
## graph is a variable showing the graph structure and every node and its neighbors are in a dictionary with their edge weights
## start specifies the starting node

## this concludes the 4.21 section a, and there are two ways of doing it, well really one, but one took less effort than the other

## 4.21 b) arbitrage
## similarly to part a, through research what you want to find is a negative weight cycle
## an algorithm that finds that is a Bellman-Ford Algorithm, so I will impliment that to the random graph generated above
## I will also write a version of that algorithm myself

def cycleExists():
    numOfCurrencies = r.randint(2,20) #ideally the 20 is bigger but my laptop will explode
    print("there are ", numOfCurrencies, "currencies")
    global G
    G = nx.DiGraph()
    for i in range(int(numOfCurrencies)):
        for j in range(int(numOfCurrencies)):
            if j > i:
                iToj = r.uniform(.1,2)
                jToi = 1/ iToj
                iToj = -1 * math.log(abs(iToj))
                jToi = -1 * math.log(abs(jToi))
                iToj = (int((iToj * 10000000))) / 10000000
                jToi = (int((jToi * 10000000))) / 10000000
                G.add_edge(int(i)+1,int(j)+1, weight = iToj)
                G.add_edge(int(j)+1,int(i)+1, weight = jToi)
                print(int(i)+1, "to", int(j)+1, "weight is", iToj)
                print(int(j)+1, 'to', int(i)+1, 'weight is', jToi)
    try:
        negCycle = nx.find_negative_cycle(G, 1, weight = "weight")
        if len(negCycle) == 3:
            print('no arbitrage')
        else:
            print('there is a negative cycle and arbitrage, that cycle is... ', negCycle)
    except nx.NetworkXError:
        print('no arbitrage')
      

#Below is an example of above, with made up values and written without external libraries downloaded to ease in the graph making and traversing process

def arbitrage(graph, source):

    distances = {node: float('inf') for node in graph}
    distances[source] = 0


    for i in range(len(graph) - 1):  #updating distances if new shortest is found
        for u in graph:
            for v, weight in graph[u].items():
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight

    
    for u in graph:     
        for v, weight in graph[u].items():
            if distances[u] + weight < distances[v]:
                return True

    return False

# Example b/c I cannot find real usuauble data 

exchange_rates = {
    'USD': {'EUR': -1 * 0.85, 'JPY': -1 * 110.25},
    'EUR': {'USD': -1 * (1/0.85), 'JPY': -1 * (110.25/0.85)},
    'JPY': {'USD': -1 * (1/110.25), 'EUR': -1 * (0.85/110.25)}
}

# Convert exchange rates to negative logarithm
for source in exchange_rates:
    for target in exchange_rates[source]:
        if exchange_rates[source][target] != 0:
            exchange_rates[source][target] = -1 * math.log(abs(exchange_rates[source][target]))

if arbitrage(exchange_rates, 'USD'):
    print("Profitable cycle detected!")
else:
    print("No profitable cycle found.")

exchange_rates_profitable = {
    'USD': {'EUR': 0.9, 'JPY': 0.008},
    'EUR': {'USD': 1/0.9, 'JPY': 120},
    'JPY': {'USD': 1/0.008, 'EUR': 1/120}
}

#copy and pasted from above

for source in exchange_rates:
    for target in exchange_rates[source]:
        if exchange_rates_profitable[source][target] != 0:
            exchange_rates_profitable[source][target] = -1 * math.log(abs(exchange_rates_profitable[source][target]))

if arbitrage(exchange_rates_profitable, 'USD'):
    print("Profitable cycle detected!")
else:
    print("No profitable cycle found.")


#used BF algo to look for a negative cycle
#represent the graph as a dictionary
#negative logs represent the weights of graph edges

## so i dont like that this runs off of random numbers, so I am going to use the data above, even though I know it will give and not give arbitrage, and write a program that reads those files
## then write a program that theoretically downloads data and reads it and runs those algorithms that have shown to work as intended

def noArbFromData():
    text = open(file='ratesForArb.csv')
    lines = text.readlines()
    g = nx.DiGraph()
    myList = []
    for line in lines[2:5]:
        line = line.strip().split(',')
        startCurrency = line[0]
        endCurrency = line[1]
        rate = float(line[2])
        backrate = 1/ float(line[2])
        rate = -1* math.log(abs(rate))
        backrate = -1* math.log(abs(backrate))
    g.add_edge(startCurrency,endCurrency,weight = rate) 
    g.add_edge(endCurrency,startCurrency,weight = backrate)
    try:
        negativeCycle = nx.find_negative_cycle(g, 'usd', weight = 'weight')
        if len(negativeCycle) == 3:   #this is to address this weird thing where find negative cycle addresses -0 as negative rather than 0
            print('no arbitrage')
        else:    
            print('there exists a negative cycle and arbitrage, the cycle is', negativeCycle)
    except nx.NetworkXError:
        print('no arbitrage')

def arbFromData():
    text = open(file='ratesForArb.csv')
    lines = text.readlines()
    g = nx.DiGraph()
    for line in lines[7:10]:
        line = line.strip().split(",")
        startCurrency = line[0]
        endCurrency = line[1]
        rate = float(line[2])
        backrate = 1/ float(line[2])
        rate = -1* math.log(abs(rate))
        backrate = -1* math.log(abs(backrate))
        g.add_edge(startCurrency,endCurrency,weight = rate)
        g.add_edge(endCurrency,startCurrency,weight = backrate)
    try:
        negativeCycle = nx.find_negative_cycle(g, 'usd', weight = 'weight')
        if len(negativeCycle) == 3:
            print('no arbitrage')
        else:    
            print('there exists a negative cycle and arbitrage, the cycle is', negativeCycle)
    except nx.NetworkXError:
        print('no arbitrage')


def arbFromDataDownload(readThisFile):
    text = open(file=readThisFile)
    lines = text.readlines()
    g = nx.DiGraph()
    for line in lines:
        line = line.strip().split(",")
        startCurrency = line[0]
        endCurrency = line[1]
        rate = float(line[2])
        backrate = 1/ float(line[2])
        rate = -1* math.log(abs(rate))
        backrate = -1* math.log(abs(backrate))
        g.add_edge(startCurrency,endCurrency,weight = rate)
        g.add_edge(endCurrency,startCurrency,weight = backrate)
    try:
        negativeCycle = nx.find_negative_cycle(g, 'usd', weight = 'weight')
        if len(negativeCycle) == 3:
            print('no arbitrage')
        else:
            print('there exists a negative cycle and arbitrage, the cycle is', negativeCycle)
    except nx.NetworkXError:
        print('no arbitrage')

import requests

## this will download a csv, from a website where I find a downloadable csv
## the idea is this could be applied to a url with usuable data and then ran every so often
## let's pretend that the data here is downloadable, and if it is, I feel very stupid
#this methodology is taken from here, I wouldn't know how to do this otherwise, https://saturncloud.io/blog/downloading-a-csv-from-a-url-and-converting-it-to-a-dataframe-using-python-pandas/

def download():
    url = 'https://data.oecd.org/conversion/exchange-rates.htm'
    response = requests.get(url)
    if response.status_code == 200:
        with open("thisFileDoesNotExist.csv", "wb") as file:
            file.write(response.content)
        print('file downloaded successfully')
    else:
        print("Failed to download CSV file. Status code:", response.status_code)
    ...
    ...
    text = open(file='thisFileDoesNotExist.csv')
    ...
    ...
    ...
    #do whatever you want with this file

#with a way to download new data established, we can now run the algorithm over and over again, assuming the data is formatted the same way
#but as we are getting the data from the same place every time this shouldn't be an issue

import threading

def makeMoney():  #downloads data and runs the arbitrage algo on it
    threading.timer(900.0, makeMoney).start #this is a timer for 15 minutes
    download()
    arbFromDataDownload("thisFileDoesNotExist.csv")

#to run this constantly just lower the frequency on the timer from 900 seconds (15 mins), to like .005 sec 

