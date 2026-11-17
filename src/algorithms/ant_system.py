from .aco_base import ACOBase
import numpy as np

class BasicAntSystem(ACOBase):
    def _update_pheromones(self, results):
        for routes, distance in results:
            delta = 1.0 / distance if distance > 0 else 0

            for route in routes:
                node = self.instance.depot_id - 1

                for next_node in route:
                    self.pheromones[node][next_node] += delta
                    self.pheromones[next_node][node] += delta
                    node = next_node
                self.pheromones[node][self.instance.depot_id - 1] += delta
                self.pheromones[self.instance.depot_id - 1][node] += delta
