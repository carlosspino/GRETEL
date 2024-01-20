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
        for i in range(self.num_instances):
            tree = nx.to_numpy_array(nx.random_tree(n=self.num_nodes_per_instance))
            infinity_cycle = self.generate_infinity_cycle()
            tree = self.join(tree, infinity_cycle)
            label = 1
            self.dataset.instances.append(GraphInstance(id=i, data=tree, label=label))
            self.context.logger.info("Generated instance with id: " + str(i))
