import networkx as nx
import matplotlib.pyplot as plt
import os
import sys

dirname = os.path.dirname(__file__)
dataDir = os.path.join(dirname, '../../data')
graphProbability = 0.25
randomSeed = 15

nxG = nx.Graph()

def generateGraphs(nodeAmount=30, edgeAmount=100):
    if not os.path.exists(dataDir):
        print(f'dataDir does not exist at {dataDir} creating data directory')
        os.makedirs(dataDir)

    graphProbability = edgeAmount / (nodeAmount * (nodeAmount - 1) / 2)
    Er = nx.erdos_renyi_graph(nodeAmount, graphProbability, randomSeed)
    filename = f'edgelist-erdos-renyi-{nodeAmount}n-{edgeAmount}e'

    try:
        filePath = os.path.join(dataDir, f'{filename}.csv')
        nx.write_edgelist(Er, filePath, delimiter=",", data=False)
    except TypeError:
        print(f'Error writing {filename} to file')

    nx.draw(Er)
    filename = os.path.join(dataDir, f'{filename}.png')
    plt.savefig(filename)

    # filePath = os.path.join(dataDir, 'edgelist-erdos-renyi-50.csv')
    # print(filePath)
    # fh = open(filePath, "rb")
    # Er2 = nx.read_edgelist(fh, delimiter=',')
    # fh.close()
    #
    # print('Er2.edges()')
    # print(nx.number_of_edges(Er2))
    # print(Er2.edges())
    #
    # nx.draw(Er2)
    # plt.savefig("network-erdos-renyi2.png")

    edgeRatio = int(edgeAmount / nodeAmount)
    Ba = nx.barabasi_albert_graph(nodeAmount, edgeRatio, randomSeed)
    filename = f'edgelist-barabasi-albert-{nodeAmount}n-{edgeAmount}e'

    try:
        filePath = os.path.join(dataDir, f'{filename}.csv')
        nx.write_edgelist(Ba, filePath, delimiter=",", data=False)
    except TypeError:
        print(f'Error writing {filename} to file')

    nx.draw(Ba)
    filename = os.path.join(dataDir, f'{filename}.png')
    plt.savefig(filename)

    edgeRatio = int((2 * edgeAmount) / nodeAmount)
    Ws = nx.watts_strogatz_graph(nodeAmount, edgeRatio, graphProbability, randomSeed)
    filename = f'edgelist-watts-strogatz-{nodeAmount}n-{edgeAmount}e'

    try:
        filePath = os.path.join(dataDir, f'{filename}.csv')
        nx.write_edgelist(Ws, filePath, delimiter=",", data=False)
    except TypeError:
        print(f'Error writing {filename} to file')

    nx.draw(Ws)
    filename = os.path.join(dataDir, f'{filename}.png')
    plt.savefig(filename)

if __name__ == '__main__':
    if (len(sys.argv) == 3):
        generateGraphs(int(sys.argv[1]), int(sys.argv[2]))
    else:
        generateGraphs()
