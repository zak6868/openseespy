import numpy as np
class Node:
    def __init__(self, id, x, y, z):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
    def coords(self):
        return np.array([self.x, self.y, self.z])

class Element:
    def __init__(self, id, node_i, node_j, area, E):
        self.id = id
        self.node_i = node_i
        self.node_j = node_j
        self.area = area
        self.E = E
    def length(self):
        return np.linalg.norm(self.node_j.coords() - self.node_i.coords())
    def direction_cosines(self):
        L = self.length()
        dx = (self.node_j.x - self.node_i.x) / L
        dy = (self.node_j.y - self.node_i.y) / L
        dz = (self.node_j.z - self.node_i.z) / L
        return np.array([dx, dy, dz])
