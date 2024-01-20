from os import listdir
from os.path import isfile, join
import numpy as np
import networkx as nx
from src.dataset.generators.base import Generator
from src.dataset.instances.graph import GraphInstance

class MCF7HGenerator(Generator):

    def init(self):
        self.num_node = self.local_config['parameters'].get('num_nodes', 100)
        self.num_edges = self.local_config['parameters'].get('num_edges', 500)
        self.num_graphs = self.local_config['parameters'].get('num_graphs', 8)

        self.adj

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

    def join(self, base, cycles):
        Ab = base
        A = Ab
        for cycle in cycles:
            A_o = cycle
            t_node = np.random.randint(0, len(Ab))
            s_node = len(A) + np.random.randint(0, len(A_o))
            A = np.block([[A, np.zeros((len(A), len(A_o)))], [np.zeros((len(A_o), len(A))), A_o]])
            A[t_node, s_node] = 1
            A[s_node, t_node] = 1
        return A
