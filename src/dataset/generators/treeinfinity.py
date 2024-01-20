import networkx as nx
import numpy as np 
from src.dataset.generators.base import Generator
from src.dataset.instances.graph import GraphInstance


class TreeInfinityCycles(Generator):

    #configuration file that passes these parameters to us
    #number of instances to generate
    #number of nodes per instance ->32 nodes per instance
    #number of nodes in the infinity cycle -> eg, 5, 6, 7

    def init(self):
        self.num_instances = self.local_config['parameters']['num_instances']
        self.num_nodes_per_instance = self.local_config['parameters']['num_nodes_per_instance']
        self.infinity_cycle_length = self.local_config['parameters']['infinity_cycle_length']    

        self.generate_dataset()

    def get_num_instances(self):
        return len(self.dataset.instances)

    def generate_infinity_cycle(self):
        half_cycle_len = self.infinity_cycle_length // 2
        g = nx.cycle_graph(half_cycle_len) # 0,1,2,...,half_cycle_len - 1
        h = nx.cycle_graph(half_cycle_len) # 0,1,2,...,half_cycle_len - 1
        h = nx.relabel_nodes(h, {i : half_cycle_len + i for i in range(max(h.nodes)+1)})
        max_nodes_g, max_nodes_h = max(g.nodes), max(h.nodes)
        common_node = self.infinity_cycle_length
        g.add_node(common_node)
        h.add_node(common_node)
        g.add_edge(max_nodes_g, common_node)
        h.add_edge(max_nodes_h, common_node)
        inf_cycle = nx.compose(g,h)
        return nx.to_numpy_array(inf_cycle)

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



    def generate_dataset(self):
        
        for i in range(self.num_instances):
            tree = nx.to_numpy_array(nx.random_tree(n=self.num_nodes_per_instance))
            #randomly choose whether the tree remains a tree or it gets an infinity cycle
            has_infinity_cycle=np.random.randint(0,2) # flip a coin in numpy

            if has_infinity_cycle:
                infinity_cycle = self.generate_infinity_cycle()
                tree = self.join(tree, infinity_cycle)
                label = 1
            else: 
                label = 0

        self.dataset.instances.append(GraphInstance(id=i, data= tree, label=0))

    def check_configuration(self):
        #manage our default parameters here
        super().check_configuration()
        local_config = self.local_config


        local_config['parameters']['num_instances'] = local_config['parameters'].get('num_instances', 1000)
        local_config['parameters']['num_nodes_per_instance'] = local_config['paramaters'].get('num_nodes_per_instances', 32)
        local_config['parameters']['infinity_cycle_length'] = local_config['paramaters'].get('infinity_cycle_length', 6)

        assert(int(local_config['parameteres']['infinity_cycle_length']) // 2 >= 3)

        


