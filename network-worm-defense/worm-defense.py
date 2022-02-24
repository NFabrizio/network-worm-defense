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

def getInoculatedNodes(graph):
    return [node for node,nodeState in graph.nodes(data=True) if nodeState['isInoculated'] == True]

def wormDefense(networkCSV, infectionProbability = 0.5, infectionStartNode = 1,  inoculationProbability = 0.5, inoculationStartNode = 1, debug=False):
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
        filename = f'erdos-renyi-{infectionProbability}'
        filePath = os.path.join(dataDir, f'{filename}.png')
        print(f'Network graph visualization saved at {filePath}')
        plt.savefig(filePath)

    # Instantiate infected nodes list, time period counter
    infectedNodesList = []
    inoculatedNodesList = []
    timePeriods = 0

    nx.set_node_attributes(NetworkGraph, False, 'isInfected')
    nx.set_node_attributes(NetworkGraph, False, 'isInoculated')

    if (debug):
        print('Initial list of infected nodes:')
        print(getInfectedNodes(NetworkGraph))
        print(getInoculatedNodes(NetworkGraph))

        print('List of nodes in network graph:')
        for node in nx.nodes(NetworkGraph):
            print(node)
        print('List of infection start node neighboring nodes in network graph:')
        print(nx.neighbors(NetworkGraph, infectionStartNode))
        print('List of inoculation start node neighboring nodes in network graph:')
        print(nx.neighbors(NetworkGraph, inoculationStartNode))
        print('Data stored for inoculation start node:')
        print(NetworkGraph.nodes[inoculationStartNode])
        print('Data stored for all nodes in network graph:')
        print(NetworkGraph.nodes(data=True))

    # Change state of infectionStartNode to infected
    NetworkGraph.nodes[infectionStartNode]['isInfected'] = True

    # Change state of inoculationStartNode to infected
    NetworkGraph.nodes[inoculationStartNode]['isInoculated'] = True

    if (debug):
        print('Data stored for infection start node after infection:')
        print(NetworkGraph.nodes[infectionStartNode])
        print('List of infected nodes after initial infection:')
        print(getInfectedNodes(NetworkGraph))
        print(f'Number of infected nodes: {len(getInfectedNodes(NetworkGraph))}')
        print('Data stored for inoculation start node after inoculation:')
        print(NetworkGraph.nodes[inoculationStartNode])
        print('List of inoculated nodes after initial inoculation:')
        print(getInoculatedNodes(NetworkGraph))
        print(f'Number of inoculated nodes: {len(getInoculatedNodes(NetworkGraph))}')

    while ((len(getInfectedNodes(NetworkGraph)) > 0) and (len(getInfectedNodes(NetworkGraph)) < totalNodes)):
        # Get list of all infected nodes
        infectedNodesList = getInfectedNodes(NetworkGraph)
        # Get list of all inoculated nodes
        inoculatedNodesList = getInoculatedNodes(NetworkGraph)

        # Record time period, number of infected nodes and  number of inoculated nodes
        recordData.append((timePeriods, len(infectedNodesList), len(inoculatedNodesList)))

        for sourceNode in infectedNodesList:
            for neighbor in nx.neighbors(NetworkGraph, sourceNode):
                # For each neighboring node, randomly infect it based on infectionProbability
                if ((NetworkGraph.nodes[neighbor]['isInoculated'] == False) and (NetworkGraph.nodes[neighbor]['isInfected'] == False) and (random.random() < infectionProbability)):
                    NetworkGraph.nodes[neighbor]['isInfected'] = True

        for sourceNode in inoculatedNodesList:
            for neighbor in nx.neighbors(NetworkGraph, sourceNode):
                # For each neighboring node, randomly inoculate it based on inoculationProbability
                if ((NetworkGraph.nodes[neighbor]['isInoculated'] == False) and (random.random() < inoculationProbability)):
                    NetworkGraph.nodes[neighbor]['isInoculated'] = True
                    NetworkGraph.nodes[neighbor]['isInfected'] = False

        timePeriods += 1

    infectedNodesList = getInfectedNodes(NetworkGraph)
    inoculatedNodesList = getInoculatedNodes(NetworkGraph)

    # Record time period and number of infected nodes
    recordData.append((timePeriods, len(infectedNodesList), len(inoculatedNodesList)))

    if (debug):
        print('Final list of infected nodes:')
        print(infectedNodesList)
        print('Final list of inoculated nodes:')
        print(inoculatedNodesList)

    print(f'Final count of infected nodes: {len(infectedNodesList)}')
    print(f'Final count of inoculated nodes: {len(inoculatedNodesList)}')
    print(f'timePeriods: {timePeriods}')

    print('Infection and inoculation over time:')
    for record in recordData:
        print(record)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This application simulates the spread of a worm virus through a network by randomly infecting neighboring nodes')

    parser.add_argument('networkCSV', type=pathlib.Path, help='Absolute path to CSV file containing network edge list')
    parser.add_argument('infectionProbability', type=float, nargs='?', help='Optional. Float value representing infection probability of selected node infection. Default: 0.5')
    parser.add_argument('infectionStartNode', nargs='?', help='Optional. Integer value representing node from which network infection will start. Default: 1')
    parser.add_argument('inoculationProbability', type=float, nargs='?', help='Optional. Float value representing inoculation probability of selected node inoculation. Default: 0.5')
    parser.add_argument('inoculationStartNode', nargs='?', help='Optional. Integer value representing node from which network inoculation will start. Default: 1')
    parser.add_argument('--debug', action='store_true', help='Optional switch. Switch that determines whether to run application in debug mode. Default: False')

    args = parser.parse_args()

    if not os.path.isabs(args.networkCSV):
        parser.error("First arg must be an absolute path to a CSV file. Ex. /Users/jsmith/path/to/network/csv/file.csv")

    # propagateWorm(*sys.argv[1:])
    wormDefense(networkCSV=args.networkCSV, infectionProbability=args.infectionProbability, infectionStartNode=args.infectionStartNode,  inoculationProbability=args.inoculationProbability, inoculationStartNode=args.inoculationStartNode, debug=args.debug)
