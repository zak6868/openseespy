import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from model import Node, Element
import openseespylinux.opensees as ops

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

    def generate_regular_building(self, m, n, dx=1, dy=1, dz=1, mode="2D", A=1, E=1):
        self.nodes = []
        self.elements = []
        self.mode = mode

        if mode == "2D":
            for floor in range(n):
                for i in range(m):
                    self.add_node(i * dx, 0, floor * dz)

            for floor in range(n - 1):
                base = floor * m
                next_base = (floor + 1) * m
                for i in range(m):
                    self.add_element(base + i, next_base + i, A, E)

            for floor in range(n):
                base = floor * m
                for i in range(m - 1):
                    self.add_element(base + i, base + i + 1, A, E)

        elif mode == "3D":
            per_floor = m * m

            for floor in range(n):
                for ix in range(m):
                    for iy in range(m):
                        self.add_node(ix * dx, iy * dy, floor * dz)

            for floor in range(n - 1):
                base = floor * per_floor
                next_base = (floor + 1) * per_floor
                for k in range(per_floor):
                    self.add_element(base + k, next_base + k, A, E)

            for floor in range(n):
                base = floor * per_floor
                for ix in range(m - 1):
                    for iy in range(m):
                        n1 = base + ix * m + iy
                        n2 = base + (ix + 1) * m + iy
                        self.add_element(n1, n2, A, E)

            for floor in range(n):
                base = floor * per_floor
                for ix in range(m):
                    for iy in range(m - 1):
                        n1 = base + ix * m + iy
                        n2 = base + ix * m + (iy + 1)
                        self.add_element(n1, n2, A, E)

        else:
            raise ValueError("mode must be '2D' or '3D'")

    def plot(self):
        if self.mode == "2D":
            fig, ax = plt.subplots()
            for e in self.elements:
                ax.plot([e.node_i.x, e.node_j.x],
                        [e.node_i.z, e.node_j.z], 'b-')
            ax.set_aspect('equal')
            ax.set_xlabel("x")
            ax.set_ylabel("z")
            plt.show()

        else:
            fig = plt.figure(figsize=(5,5))
            ax = fig.add_subplot(111, projection='3d')
            for e in self.elements:
                ax.plot([e.node_i.x, e.node_j.x],
                        [e.node_i.y, e.node_j.y],
                        [e.node_i.z, e.node_j.z], 'b-')

            xs = [n.x for n in self.nodes]
            ys = [n.y for n in self.nodes]
            zs = [n.z for n in self.nodes]

            max_range = max(
                max(xs) - min(xs),
                max(ys) - min(ys),
                max(zs) - min(zs)
            ) / 2

            mid_x = (max(xs) + min(xs)) / 2
            mid_y = (max(ys) + min(ys)) / 2
            mid_z = (max(zs) + min(zs)) / 2

            ax.set_xlim(mid_x - max_range, mid_x + max_range)
            ax.set_ylim(mid_y - max_range, mid_y + max_range)
            ax.set_zlim(mid_z - max_range, mid_z + max_range)
            ax.grid(False)
            plt.show()
    def to_opensees(self):

        ops.wipe()
        ops.model('basic', '-ndm', 3, '-ndf', 6)

        # --- Nodes
        for n in self.nodes:
            ops.node(n.id, n.x, n.y, n.z)
            ops.fix(n.id, *n.fix)
            if n.mass is not None:
                ops.mass(n.id, *n.mass)

        # --- Material pour truss (E=1.0 ne sert qu'identification)
        ops.uniaxialMaterial("Elastic", 1, 1.0)

        # --- Transformation pour beams
        ops.geomTransf("Linear", 1, 0, 0, 1)

        # --- Elements
        for e in self.elements:
            ni = e.node_i.id
            nj = e.node_j.id

            if e.etype == "truss":
                ops.element("truss", e.id, ni, nj, e.area, 1)

            elif e.etype == "beam":
                if any(v is None for v in [e.G, e.J, e.Iy, e.Iz]):
                    raise ValueError(
                        f"Beam element {e.id} is missing G, J, Iy, or Iz."
                    )

                ops.element("elasticBeamColumn",
                            e.id, ni, nj,
                            e.area, e.E, e.G, e.J, e.Iy, e.Iz,
                            1)

            else:
                raise ValueError(f"Unknown element type: {e.etype}")

        return ops


