import numpy as np
import networkx as nx
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
        #We want to extract edges from MCF7H_A.txt
        #Method for reading lines, like a scanner
        edges = open(self.edg_file_path,'r').readLines()
        arcs = []

        for edges in arcs:
            #We split each node_id by a , and then another line
            edges_list = edges.split(',')
            #We add to the list 
            arcs.append((int(edges[0].strip)),int(edges[1].strip()))
    

        #The number of a line is a graph_id, its value is the graph class
        gr_labels = open(self.grph_file_path, 'r').readlines()
        graphs = []
        
        #There is no need of spliting the line because there is just a class value
        for label in gr_labels:
            graphs.append(int(label.strip()))







