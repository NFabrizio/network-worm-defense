#!/usr/bin/python

import argparse
import matplotlib.pyplot as plt
import networkx as nx
import os
import pathlib
import random
import sys

dirname = os.path.abspath(os.path.dirname(__file__))
dataDir = os.path.join(dirname, '../data')

def getInfectedNodes(graph):
    return [node for node,nodeState in graph.nodes(data=True) if nodeState['isInfected'] == True]

def propagateWorm(networkCSV, probability = 0.5, startNode = 1, debug=False):
    inputFile = os.path.join(dirname, networkCSV)
    totalNodes = 0
    recordData = []

    if (debug):
        print(f'Data directory path: {dataDir}')
        print(f'Network CSV file path: {inputFile}')

    fh = open(inputFile, "rb")
    # file_contents = fh.read()
    # print(file_contents)
    NetworkGraph = nx.read_edgelist(fh, delimiter=',')
    fh.close()

    totalNodes = len(NetworkGraph.nodes)
    print(f'Number of nodes in network graph: {totalNodes}')

    if (debug):
        print(f'Number of edges in network: {nx.number_of_edges(NetworkGraph)}')
        print('Network graph edge list:')
        print(NetworkGraph.edges())

        nx.draw(NetworkGraph)
        # TODO: Use input file name as filename
        filename = f'erdos-renyi-{probability}'
        filePath = os.path.join(dataDir, f'{filename}.png')
        print(f'Network graph visualization saved at {filePath}')
        plt.savefig(filePath)

    # Instantiate infected nodes list, time period counter
    infectedNodesList = []
    timePeriods = 0
    nx.set_node_attributes(NetworkGraph, False, 'isInfected')

    if (debug):
        print('Initial list of infected nodes:')
        print(getInfectedNodes(NetworkGraph))

        print('List of nodes in network graph:')
        for node in nx.nodes(NetworkGraph):
            print(node)
        print('List of start node neighboring nodes in network graph:')
        print(nx.neighbors(NetworkGraph, startNode))
        print('Data stored for start node:')
        print(NetworkGraph.nodes[startNode])
        print('Data stored for all nodes in network graph:')
        print(NetworkGraph.nodes(data=True))

    # Change state of startNode to infected
    NetworkGraph.nodes[startNode]['isInfected'] = True

    if (debug):
        print('Data stored for start node after infection:')
        print(NetworkGraph.nodes[startNode])
        print('List of infected nodes after initial infection:')
        print(getInfectedNodes(NetworkGraph))
        print(f'Number of infected nodes: {len(getInfectedNodes(NetworkGraph))}')

    while (len(getInfectedNodes(NetworkGraph)) < totalNodes):
        # For each infected node, get neighboring node list
        infectedNodesList = getInfectedNodes(NetworkGraph)

        # Record time period and number of infected nodes
        recordData.append((timePeriods, len(infectedNodesList)))

        for sourceNode in infectedNodesList:
            for neighbor in nx.neighbors(NetworkGraph, sourceNode):
                # For each neighboring node, randomly infect it based on probability
                if ((NetworkGraph.nodes[neighbor]['isInfected'] == False) and (random.random() < probability)):
                    NetworkGraph.nodes[neighbor]['isInfected'] = True

        timePeriods += 1

    infectedNodesList = getInfectedNodes(NetworkGraph)
    # infectedNodesList.sort()

    # Record time period and number of infected nodes
    recordData.append((timePeriods, len(infectedNodesList)))

    if (debug):
        print('Final list of infected nodes:')
        print(infectedNodesList)

    print(f'Final count of infected nodes: {len(infectedNodesList)}')
    print(f'timePeriods: {timePeriods}')

    print('Infection over time:')
    for record in recordData:
        print(record)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This application simulates the spread of a worm virus through a network by randomly infecting neighboring nodes')

    parser.add_argument('networkCSV', type=pathlib.Path, help='Absolute path to CSV file containing network edge list')
    parser.add_argument('probability', type=float, nargs='?', help='Optional. Float value representing probability selected node infection. Default: 0.5')
    parser.add_argument('startNode', nargs='?', help='Optional. Integer value representing node from which network infection will start. Default: 1')
    parser.add_argument('--debug', action='store_true', help='Optional switch. Switch that determines whether to run application in debug mode. Default: False')

    args = parser.parse_args()

    if not os.path.isabs(args.networkCSV):
        parser.error("First arg must be an absolute path to a CSV file. Ex. /Users/jsmith/path/to/network/csv/file.csv")

    # propagateWorm(*sys.argv[1:])
    propagateWorm(networkCSV=args.networkCSV, probability=args.probability, startNode=args.startNode, debug=args.debug)
