class Motif:
    def __init__(self, local_nodes, edges):
        self.local_nodes = local_nodes
        self.edges = edges

    def can_apply(self, model, origin_node_id, dx, dy, dz):
        return True

    def apply_to_model(self, model, origin_node_id, dx, dy, dz, area, E):
        origin = model.nodes[origin_node_id]
        base_x, base_y, base_z = origin.x, origin.y, origin.z

        coords = []
        for local in self.local_nodes:
            if len(local) == 2:      # Motif 2D : (lx, lz)
                lx, lz = local
                x = base_x + lx * dx
                y = base_y            # y = 0 en 2D
                z = base_z + lz * dz

            elif len(local) == 3:    # Motif 3D : (lx, ly, lz)
                lx, ly, lz = local
                x = base_x + lx * dx
                y = base_y + ly * dy
                z = base_z + lz * dz

            else:
                raise ValueError("local_nodes must be tuples of size 2 (2D) or 3 (3D)")

            coords.append((x, y, z))

        id_map = {}
        for i, (x, y, z) in enumerate(coords):
            found = None
            for node in model.nodes:
                if abs(node.x-x)<1e-6 and abs(node.y-y)<1e-6 and abs(node.z-z)<1e-6:
                    found = node.id
                    break
            if found is None:
                model.add_node(x, y, z)
                found = model.nodes[-1].id
            id_map[i] = found

        for (i, j) in self.edges:
            ni, nj = id_map[i], id_map[j]
            exists = False
            for e in model.elements:
                if (e.node_i.id==ni and e.node_j.id==nj) or (e.node_i.id==nj and e.node_j.id==ni):
                    exists = True
                    break
            if not exists:
                model.add_element(ni, nj, area, E)

