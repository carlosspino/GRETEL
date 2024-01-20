import numpy as np
from src.dataset.generators.base import Generator
from src.dataset.instances.graph import GraphInstance

class MCF7HGenerator(Generator):
    
    def init(self):
        self.num_instances = self.local_config['parameters'].get('num_instances', 1000)
        self.graph_folder = 'path/to/MCF-7H/dataset'  # Reemplaza con la ruta real a tu conjunto de datos
        self.generate_dataset()

    def check_configuration(self):
        super().check_configuration()
        local_config = self.local_config
        local_config['parameters']['num_instances'] = local_config['parameters'].get('num_instances', 1000)

    def generate_dataset(self):
        for i in range(self.num_instances):
            try:
                # Cargar la estructura de adyacencia del grafo desde DS_A.txt
                adj_matrix = np.loadtxt(f'{self.graph_folder}/DS_A.txt', delimiter=',', dtype=int)
            except Exception as e:
                print(f"Error loading the file: {e}")
                continue  # Si hay un error, pasa a la siguiente iteración

            # Crear una instancia de grafo
            graph_instance = GraphInstance(id=i, data=adj_matrix, label=0)
            self.dataset.instances.append(graph_instance)

            self.context.logger.info("Generated instance with id:" + str(i))
