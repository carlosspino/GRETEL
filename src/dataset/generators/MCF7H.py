import networkx as nx
import numpy as np
from src.dataset.generators.base import Generator
from src.dataset.instances.graph import GraphInstance
import os
from os import listdir
from os.path import isfile, join
class MCF7HGenerator(Generator):

    def init(self):

        # Obtén la ruta del directorio actual del script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construye la ruta al directorio del dataset MCF7H dentro del proyecto Gretel
        base_path = os.path.join(script_dir, 'data', 'datasets', 'MCF7H')

        #PATH to the MCF7H dataset
        #We save in variables each path
        self.edg_file_path = os.path.join(base_path, 'MCF7H_A.txt')
        self.nod_file_path = os.path.join(base_path, 'MCF7H_graph_indicator.txt')
        self.grph_file_path = os.path.join(base_path, 'MCF7H_graph_labels.txt')
        self._nlbls_file_path = os.path.join(base_path, 'MCF7H_node_labels.txt')
        self._edlbls_file_path = os.path.join(base_path, 'MCF7H_edge_labels.txt')

        #Generate dataset
        self.generate_dataset()

        
    def get_num_instances(self):
        return len(self.dataset.instances)


    def generate_dataset(self):
        #We create a dictionary called g (graph)
        g = {}
        #Loop with the number of nodes, we instance an array with 27770 graphs
        for k in np.arange(1, 27770):
            g[k] = np.array([]).reshape([-1,2])
        #We create an array
        g_ind=np.array([])
        with open(self.nod_file_path) as graph_indicator_file:
            lines = graph_indicator_file.readlines()
            for i in lines:
                gId=int(i)
                g_ind=np.append(g_ind,gId)
        
        with open(self.edg_file_path) as A_file:
            lines = A_file.readlines()
            for i in lines:
                tuples = i.split(', ')
                n1 = int(tuples[0])
                n2 = int(tuples[1])
                g[g_ind[n1-1]]=np.vstack([g[g_ind[n1-1]],[n1,n2]])

        lbs = np.array([])
        	
            
        with open(self.grph_file_path) as graphlabel_file:
            lines = graphlabel_file.readlines()
            # Iterate through the lines
            for i in lines:
                # Get the label
                l=int(i)
                # Add the label to the labels array
                lbs=np.append(lbs,l)

        length_graphs = []
        for i in np.arange(1,27770):
            length_graphs.append(g[i].max()-g[i].min()) #El numero de nodos que hay en cada posición de graphs

        for i in np.arange(1, 27770): 
            dt=self.create_adj_mat(g[i])
            self.dataset.instances.append(GraphInstance(id=i, data=dt, label=int(lbs[i-1])))