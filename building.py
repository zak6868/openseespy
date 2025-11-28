import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from model import Node, Element

class BuildingModel:
    def __init__(self):
        self.nodes = []
        self.elements = []
        self.mode = "2D"

    def add_node(self, x, y, z):
        self.nodes.append(Node(len(self.nodes), x, y, z))

    def add_element(self, node_i_id, node_j_id, area, E):
        node_i = self.nodes[node_i_id]
        node_j = self.nodes[node_j_id]
        self.elements.append(Element(len(self.elements), node_i, node_j, area, E))

    def plot(self):
        if self.mode == "2D":
            fig, ax = plt.subplots()
            for e in self.elements:
                ax.plot([e.node_i.x, e.node_j.x],
                        [e.node_i.z, e.node_j.z], 'b-')
            ax.set_xlabel("x")
            ax.set_ylabel("z")
            ax.set_aspect("equal")
            plt.show()

        else:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            for e in self.elements:
                ax.plot([e.node_i.x, e.node_j.x],
                        [e.node_i.y, e.node_j.y],
                        [e.node_i.z, e.node_j.z], 'b-')
            plt.show()

    def generate_regular_building(self, m, n, dx=1, dy=0, dz=1, mode="2D", A=1, E=1):
        self.nodes = []
        self.elements = []
        self.mode = mode

        if mode == "2D":
            for floor in range(n):
                for i in range(m):
                    self.add_node(i*dx, 0, floor*dz)

            for floor in range(n-1):
                base = floor*m
                next_base = (floor+1)*m
                for i in range(m):
                    self.add_element(base+i, next_base+i, A, E)

            for floor in range(n):
                base = floor*m
                for i in range(m-1):
                    self.add_element(base+i, base+i+1, A, E)
