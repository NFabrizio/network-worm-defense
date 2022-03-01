# network-worm-defense

A program that simulates how a software worm propagates in a computer network and
infects machines. This application can be used to run two types of simulations: worm
propagation with no defense and worm propagation with defense. This application also
includes a utility to create network structures.

_Authors_: [Nick Fabrizio](https://github.com/NFabrizio)

Project is written in Python, and uses the NetworkX package for network creation
and manipulation.

## Environment Set Up

_Python is required to run this application, and Python 3.8.9+ is highly recommended._
_Pip version 22.0.3 is required to run this application._

1. Clone this repository to your local environment.
   _If you already have the files downloaded to your local machine, skip to the next step._
2. Fork this Github repo.
   1. In a web browser, visit https://github.com/NFabrizio/network-worm-defense
   2. Click the Fork button in the upper right corner of the screen
   3. In the "Where should we fork this repository?" pop up, select your username.
      Github should create a fork of the repo in your account
3. Clone your fork of the network-worm-defense repo.
   1. In the terminal on your local environment, navigate to the directory where
      you want to clone the network-worm-defense repo
      `cd ~/path/to/your/directory`
   2. In the terminal, run:
      `git clone [clone-url-for-your-fork]`
      The URL should be in the format git@github.com:YourUsername/network-worm-defense.git
4. Install the required Python packages in your Python environment.
5. In the terminal on your local environment, navigate to the directory where
   the network-worm-defense files are located.
6. In the terminal run the following command to install the required packages.
   `pip3 install -r requirements.txt`
   _If any errors are encountered while running this command, try upgrading your pip version using `pip install --upgrade pip`_

## Usage

This application can be used to run three separate programs: worm propagation,
worm defense and network CSV generation. Below are the usage instructions for
each of these programs.

### Worm Propagation

This program runs a simulation on a network to show worm propagation through the
network when there is no worm defense mechanism in place. In the program, a
network is created from a user provided CSV file using the NetworkX Python package.
Worm infection is represented by setting the value of the node attribute with the
name “isInfected” to True. Once the data for the first infected node is properly
set, the program enters a loop in which it retrieves a list of nodes neighboring
any infected node from the network. For each of these neighboring nodes, a random
float is generated, and if it is less than the probability of infection provided
in the arguments, the value of the “isInfected” attribute for that node is also
set to True. Once all neighbors of all infected nodes have been visited by the
worm, one iteration of the loop ends. This is considered one time cycle. The loop
continues until all nodes in the network have been infected. The program output is
a list of time cycles and the cummulative number of infected nodes at that time cycle.

To run this program from the command line, run:
`python3 worm-propagation.py [csvFileLocation] [probability] [startNode]`

Arguments:

```
csvFileLocation       Required. String. Absolute path to location of a CSV file containing list of tuples representing the edges within the network
probability           Optional. Float. Probability that the worm will infect an uninfected node. Default: 0.5
startNode             Optional. Integer. Index of the initial infected node from where the worm starts infecting. Default: 1
```

Sample usage:
`python3 path/to/network-worm-defense/worm-propagation.py /absolute/path/to/your-network-csv-file.csv 0.1 19`

### Worm Defense

This program is similar to the worm propagation program with the added feature
of the worm defense spreading through the network in a similar manner to the
software worm. In each iteration of the loop, any nodes neighboring an inoculated
node are randomly inoculated using the inoculation probability. This is
implemented by setting the value of the node attribute with the name
“isInoculated” to True and the value of the node attribute with the name
“isInfected” to False. Once inoculated, a node is cured from an infection, if it
has one, and it can no longer be infected by the software worm. In this program,
the loop continues if there is at least one infected and one non-infected node
in the network. The program output is a list of time cycles and the cummulative
number of infected and inoculated nodes at that time cycle.

To run this program from the command line, run:
`python3 worm-defense.py [csvFileLocation] [infectionProbability] [infectionStartNode] [inoculationProbability] [inoculationStartNode]`

Arguments:

```
csvFileLocation         Required. String. Absolute path to location of a CSV file containing list of tuples representing the edges within the network
infectionProbability    Optional. Float. Probability that the worm will infect an uninfected node. Default: 0.5
infectionStartNode      Optional. Integer. Index of the initial infected node from where the worm starts infecting. Default: 1
inoculationProbability  Optional. Float. Probability that the worm defense will inoculate an un-inoculated node. Default: 0.5
inoculationStartNode    Optional. Integer. Index of the initial inoculated node from where the worm defense starts inoculating. Default: 1
```

Sample usage:
`python3 path/to/network-worm-defense/worm-defense.py /absolute/path/to/your-network-csv-file.csv 0.1 19 0.1 123`

### Network CSV Generation

This utility program generates CSV files containing tuples that represent network edges
for each of the following network types: Erdös-Rényi, Barabási-Albert and
Watts-Strogatz. In addition, it creates a PNG file with a visual representation
of the network. A random seed number is hard coded into this program so that the
same network files are created consistently.
**Note: This program will create a data directory in the root of the project (i.e., two directories up from /utils) if one does not exist**

To run this program from the command line, run:
`python3 utils/networkCSVGenerator.py [numberOfNodes] [numberOfEdges]`

Arguments:

```
numberOfNodes         Optional. Integer. Number of nodes desired in the network. Default: 30
numberOfEdges         Optional. Integer. Number of edges desired in the network. Default: 100
```

Sample usage:
`python3 path/to/network-worm-defense/utils/networkCSVGenerator.py 500 1000`

## Docs

View the project assignment description under the [docs/](docs) directory
