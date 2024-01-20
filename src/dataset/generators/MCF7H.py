import numpy as np
import networkx as nx
from src.dataset.generators.base import Generator
from src.dataset.instances.graph import GraphInstance

class MCF7HGenerator(Generator):

    def init(self):
        self.num_instances = self.local_config['parameters'].get('num_instances', 1000)
        self.num_nodes_per_instance = self.local_config['parameters'].get('num_nodes_per_instance', 32)
        self.infinity_cycle_length = self.local_config['parameters'].get('infinity_cycle_length', 6)
        self.generate_dataset()

    def get_num_instances(self):
        return len(self.dataset.instances)

    def generate_infinity_cycle(self):
        half_cycle_len = self.infinity_cycle_length // 2
        g = nx.cycle_graph(half_cycle_len)
        h = nx.cycle_graph(half_cycle_len)
        h = nx.relabel_nodes(h, {i: half_cycle_len + i for i in range(max(h.nodes) + 1)})
        max_nodes_g, max_nodes_h = max(g.nodes), max(h.nodes)
        common_node = self.infinity_cycle_length
        g.add_node(common_node)
        h.add_node(common_node)
        g.add_edge(max_nodes_g, common_node)
        h.add_edge(max_nodes_h, common_node)
        inf_cycle = nx.compose(g, h)
        return nx.to_numpy_array(inf_cycle)

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
