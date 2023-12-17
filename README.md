# Combinatorial Optimization Project
## Introduction
This project has been created for the course of Numerical In Python at the ESIEA engineering school. The goal of this project is to solve the problem of the maximum clique in a graph. The maximum clique problem is the problem of finding the largest subset of vertices in an undirected graph that are mutually adjacent. The maximum clique problem is NP-complete and has many applications in various fields. The project is divided into several parts including :
- The creation of an optimized linear model
- The creation a glpk solvable file
- The development of a greedy algorithm
- The development of a genetic algorithm
- The development of at least one other metaheuristic algorithm (HERE : Ant Colony Optimization)
- Research about other metaheuristic algorithms and heuristics
- Research about result and comparison between the different algorithms

## Installation
To install the project, you need to clone the repository and install the requirements (glpk, python3)

The project is also available on [GitHub](https://github.com/Keyraus/NumericalTop1), as a project or a release. ([Link to the release](https://github.com/Keyraus/NumericalTop1/releases))

## Usage
Each file contains methods associated with their name.

The only launchable files are :
- convertion.py
- debuggerAlgorithms.py
- main.py

Those files are different in usage and are described below

### convertion.py
This file is used to convert a graph file into a glpk solvable file. The file must be in the following format :
```bash
python3 convertion.py <path_to_graph_file> <path_to_output_file>
```
The output file will be a .lp file that can be used by glpk

### debuggerAlgorithms.py
This file is used to test the different algorithms. It will run the different algorithms on the same graph and compare the results. The file must be in the following format :
```bash
python3 debuggerAlgorithms.py <path_to_graph_file> <time_limit> <path_to_result_of_glpk>
```
The path of the result of glpk is used to compare the results of the algorithms with the optimal solution. The time limit is used to stop the algorithms if they are too long.

### main.py
This file is used to run the best algorithm on a graph. The file must be in the following format :
```bash
python3 main.py <time_limit> <path_to_graph_file> <path_to_output_file>
```
The time limit is used to stop the algorithm if it is too long. The output file will be a .txt file containing the result of the algorithm.

## Implemented algorithms
### Greedy
The greedy algorithm is a simple algorithm that will take the first powerfull (its weight by the number of relations he has)vertex of the graph and add it to the clique. Then, it will take the next vertex most powerfull that knows everybody in the clique and add it to the clique. It will repeat this process until there is no more vertex to add to the clique.
### Genetic
The genetic algorithm is an algorithm that will create a population of clique. Then, it will select the best clique of the population and create a new population from it by doing multiple thing like mutation. It will repeat this process until the time limit is reached.
### Ant Colony Optimization
The ant colony optimization algorithm is an algorithm that will create a population of clique. Then, it will select the best clique of the population and create a new population with it. It will repeat this process until the time limit is reached.
### Bron-Kerbosch algorithm
The Bron-Kerbosch algorithm is an algorithm that will create a population of clique. Then, it will select the best clique of the population and create a new population with it. 

## Results
The results of the glpk ran on the graphs are in the folder "Solutions". The results of the glpk are not present in the release of the GitHub repository because of the size of the files.

A word document containing the researchs exists somewhere over the rainbow.

## Contributors
- [Cédric MARTY](https://github.com/Keyraus)
- [Bastien TAROT](https://github.com/Suna24)
- [Guénaël LE ROUX](https://github.com/guenael-lr)
- [Antonin AUBERT](https://github.com/Grizfreak)