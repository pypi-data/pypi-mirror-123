import numpy as np

from random import choice

from pge.model.spreading.spreader.fix_size import FixSpreadModel


class UniformFixGossip(FixSpreadModel):
    def choice_node(self):
        return choice(self.ids)

    def iteration(self):
        node = self.choice_node()
        if self.in_direct:
            others = self.graph.get_in_degrees(node)
        else:
            others = self.graph.get_out_degrees(node)

        if others.size != 0:
            u = choice(others)
            self.received[u].update(self.received[node])


class Uniform1KnownFixGossip(UniformFixGossip):
    def choice_node(self):
        return choice([node for node in self.received.keys() if len(self.received[node]) > 0])

    def iteration(self):
        node = self.choice_node()
        if self.in_direct:
            others = self.graph.get_in_degrees(node)
        elif self.in_direct is None:
            others = np.append(self.graph.get_in_degrees(node), self.graph.get_out_degrees(node))
        else:
            others = self.graph.get_out_degrees(node)

        if others.size != 0:
            u = choice(others)
            (self.received[u]).update(self.received[node])
