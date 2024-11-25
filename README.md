# Greedy Algorithm for Independent Set 
## Ideas 
- The [independent set problem](https://en.wikipedia.org/wiki/Independent_set_(graph_theory)) asks for the largest subset of vertices in a graph such that no two vertices in the subset are adjacent. 
- A random algorithm provides a simple approach to this problem. 
    - It selects vertices at random and removes them along with their neighbors until the graph is empty.


## Installation
- Requires: python
1. Clone the repository

2. Install the requirements
    ```
    pip install -r  requirements.txt 
    ```

3. Run the script
    ```
    python independent-set.py
    ```
    Note:
    - Explore changing the variables on lines 87-91 to customize the outputs


## Key Components 

#### Random Selection:
- Vertices are selected at random.


#### Bipartite Graph:
A bipartite graph is a special type of graph where nodes can be divided into two distinct sets, 
𝐴 and 𝐵, such that every edge connects a node in set 𝐴 to a node in set 𝐵. There are no edges between nodes within the same set.

#### Key Features:
Two disjoint sets of nodes: 𝐴 and 𝐵.
Edges only exist between nodes in 𝐴 and 𝐵.

#### Code Functionality:

𝑛1: Number of nodes in set 𝐴.

𝑛2: Number of nodes in set 𝐵.

𝑑: Determines the probability of creating an edge between any pair of nodes 
(𝑎,𝑏), where 𝑎∈𝐴 and 𝑏∈𝐵. The edge probability is 𝑑/max(𝑛1,𝑛2).

- For the simulations, by default:
    - The values of d are 3,5,10
    - 𝑛1=1000, 𝑛2=1000
    - Number of simulations per 𝑑 is set to 100, via *number_simulations_per_d_value* variable

#### Performance Metrics:
- Size of the independent set.
- Composition of the set (via Graph Visuals)
- At the bottom of every file - the average for all the iterations is computed.

## Visuals 
- The output can be edited.
- Using the *save_to_one_file* boolean - this will determine if all the output is in one file or 3 seperate files for each 𝑑 value
- By default, the output will be a list of each simulation result:
    - Name of graph with iteration number
    - Total nodes in graph
    - Total nodes in independent set
    - The nodes from each set that make up the independent set (optional - use *include_list_of_nodes_in_independent_set_in_pdf*)
    - Graph visual (optional - use *graph_output* boolean)


#### Ouput:
- Images save to matplotlib_visuals folder. Within folder, each value of 𝑑 has its own folder
- pdfs save to pdf_output folder. 



