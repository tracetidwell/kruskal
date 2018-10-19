#!C:/Users/Trace/Anaconda3/envs/kruskal/python.exe
##  CSE6140 HW2
##  This assignment requires installation of networkx package if you want to make use of available graph data structures or you can write your own!!
##  Please feel free to modify this code or write your own

import networkx as nx
import time
import sys

class RunExperiments:

    def read_graph(self, filename):
        #make sure to add to filename the directory where it is located and the extension .txt
        #G = nx.MultiGraph()
        #if you want to use networkx

        #Write code to add nodes and edges
        #Check out add_node, add_edge in networkx
        graph = nx.MultiGraph()
                
        with open(filename) as g:
            g.readline()

            for line in g:
                edge_data = list(map(lambda x: int(x), line.split()))
                u, v, weight = edge_data[0], edge_data[1], edge_data[2]
                graph.add_edge(u, v, weight=weight)

        return graph

    def find_sets(self, u, v, vertex_sets):
        u_idx = -1
        v_idx = -1

        for idx, vertex_set in vertex_sets.items():
            if u in vertex_set:
                u_idx = idx
            if v in vertex_set:
                v_idx = idx
            if u_idx > -1 and v_idx > -1:
                return u_idx, v_idx
        return u_idx, v_idx

    def computeMST(self, graph):
        graph.mst = nx.Graph()
        graph.cost = 0
        vertex_sets = {}
        
        for node in graph.nodes:
            vertex_sets[node] = {node}
            
        for u, v, weight in sorted(list(graph.edges(data='weight')), key=lambda edge: edge[2]):
            u_set, v_set = self.find_sets(u, v, vertex_sets)
            
            if u_set != v_set:
                graph.mst.add_edge(u, v, weight=weight)
                graph.cost += weight
                vertex_sets[u_set] = vertex_sets[u_set].union(vertex_sets[v_set])
                vertex_sets.pop(v_set)

                if len(graph.mst.edges) == len(graph) - 1:
                    return graph

        return graph

    def recomputeMST(self, u, v, weight, graph):

        if weight > max([w for u, v, w in graph.mst.edges(data='weight')]):
            graph.add_edge(u, v, weight=weight)
            return graph

        elif graph.mst.has_edge(u, v):
            if weight < graph.mst[u][v]['weight']:
                graph.cost = graph.cost - graph.mst[u][v]['weight'] + weight
                graph.mst[u][v]['weight'] = weight
                graph.add_edge(u, v, weight=weight)
                return graph
            else:
                graph.add_edge(u, v, weight=weight)
                return graph
        else:
            graph.add_edge(u, v, weight=weight)
            graph.mst.add_edge(u, v, weight=weight)
            temp = self.computeMST(graph.mst)
            if temp.cost < graph.cost:
                graph.mst = temp.mst
                graph.cost = temp.cost
            else:
                graph.mst.remove_edge(u, v)
            return graph
        
    def main(self):

        num_args = len(sys.argv)

        if num_args < 4:
            print("error: not enough input arguments")
            exit(1)

        graph_file = sys.argv[1]
        change_file = sys.argv[2]
        output_file = sys.argv[3]

        #Construct graph
        G = self.read_graph(graph_file)

        start_MST = time.time() #time in seconds
        G = self.computeMST(G) #call MST function to return total weight of MST
        total_time = (time.time() - start_MST) * 1000 #to convert to milliseconds
        #print(MSTweight, total_time)

        #Write initial MST weight and time to file
        output = open(output_file, 'w')
        output.write(str(G.cost) + " " + str(total_time) + '\n') 

        #Changes file
        with open(change_file, 'r') as changes:
            num_changes = changes.readline()

            for line in changes:             #parse edge and weight
                edge_data = list(map(lambda x: int(x), line.split()))
                assert(len(edge_data) == 3)

                u, v, weight = edge_data[0], edge_data[1], edge_data[2]

                #call recomputeMST function
                start_recompute = time.time()
                G = self.recomputeMST(u, v, weight, G)
                total_recompute = (time.time() - start_recompute) * 1000 # to convert to milliseconds
                #print(new_weight, total_recompute)

                #write new weight and time to output file
                output.write(str(G.cost) + " " + str(total_recompute) + '\n')

if __name__ == '__main__':
    # run the experiments
    #subprocess.call(["activate", 'kruskal'])
    runexp = RunExperiments()
    runexp.main()