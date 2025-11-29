from motif import Motif

motifs = {}
motifs["square_2D"] = Motif(
    local_nodes=[(0,0,0),(1,0,0),(1,0,1),(0,0,1)],
    edges=[(0,1),(1,2),(2,3),(3,0)]
)
motifs["square_2D_diag1"] = Motif(
    local_nodes=[(0,0,0),(1,0,0),(1,0,1),(0,0,1)],
    edges=[(0,1),(1,2),(2,3),(3,0),(0,2)]
)

motifs["square_2D_diag2"] = Motif(
    local_nodes=[(0,0,0),(1,0,0),(1,0,1),(0,0,1)],
    edges=[(0,1),(1,2),(2,3),(3,0),(1,3)]
)
motifs["square_2D_V"] = Motif(
    local_nodes=[(0,0,0),(0.5,0,0),(1,0,0),(1,0,1),(0,0,1)],
    edges=[(0,1),(1,2),(2,3),(3,4),(4,0),(4,1),(1,3)]
)

motifs["square_2D_INVV"] = Motif(
    local_nodes=[(0,0,0),(1,0,0),(1,0,1),(0.5,0,1),(0,0,1)],
    edges=[(0,1),(1,2),(2,3),(3,4),(4,0),(0,3),(3,1)]
)

motifs["square_2D_X"] = Motif(
    local_nodes=[(0,0,0),(1,0,0),(1,0,1),(0,0,1)],
    edges=[(0,1),(1,2),(2,3),(3,0),(1,3),(0,2)]
)

motifs["square_2D_W"] = Motif(
    local_nodes=[(0,0,0),(0.25,0,0),(0.75,0,0),(1,0,0),(1,0,1),(0.5,0,1),(0,0,1)],
    edges=[(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,0),(1,6),(1,5),(2,5),(2,4)]
)


motifs["square_2D_framedTr"] = Motif(
    local_nodes=[(0,0,0),(0.1,0,0),(0.9,0,0),(1,0,0),(1,0,0.1),(1,0,0.9),(1,0,1),(0.9,0,1),(0.1,0,1),(0,0,1),(0,0,0.9),(0,0,0.1)],
    edges=[(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10),(10,11),(11,0),(11,1),(2,4),(5,7),(8,10)]
)

motifs["horizontal_beam_x"] = Motif(
    local_nodes=[(0,0,0),(1,0,0)],
    edges=[(0,1)]
)

motifs["cube_3D"] = Motif(
    local_nodes=[
        (0,0,0),(1,0,0),(1,1,0),(0,1,0),
        (0,0,1),(1,0,1),(1,1,1),(0,1,1)
    ],
    edges=[
        (0,1),(1,2),(2,3),(3,0),
        (4,5),(5,6),(6,7),(7,4),
        (0,4),(1,5),(2,6),(3,7)
    ]
)

motifs["cube_3D_diag"] = Motif(
    local_nodes=[
        (0,0,0),(1,0,0),(1,1,0),(0,1,0),
        (0,0,1),(1,0,1),(1,1,1),(0,1,1)
    ],
    edges=[
        (0,1),(1,2),(2,3),(3,0),
        (4,5),(5,6),(6,7),(7,4),
        (0,4),(1,5),(2,6),(3,7),
        (0,6)
    ]
)

from motif import Motif

def wrap_4faces(m_south, m_east, m_north, m_west):
    motifs_2D = [m_south, m_east, m_north, m_west]

    new_nodes = []
    new_edges = []

    sizes = [len(m.local_nodes) for m in motifs_2D]
    offsets = [0]
    for k in sizes[:-1]:
        offsets.append(offsets[-1] + k)

    # Face SUD (y = 0)
    for local in m_south.local_nodes:
        if len(local) == 2:
            lx, lz = local
        else:
            lx, _, lz = local
        new_nodes.append((lx, 0, lz))

    # Face EST (x = 1)
    for local in m_east.local_nodes:
        if len(local) == 2:
            lx, lz = local
        else:
            lx, _, lz = local
        new_nodes.append((1, lx, lz))

    # Face NORD (y = 1)
    for local in m_north.local_nodes:
        if len(local) == 2:
            lx, lz = local
        else:
            lx, _, lz = local
        new_nodes.append((1 - lx, 1, lz))

    # Face OUEST (x = 0)
    for local in m_west.local_nodes:
        if len(local) == 2:
            lx, lz = local
        else:
            lx, _, lz = local
        new_nodes.append((0, 1 - lx, lz))

    # Edges internes à chaque face (aucune connexion entre faces)
    for face_id, motif in enumerate(motifs_2D):
        offset = offsets[face_id]
        for (i, j) in motif.edges:
            new_edges.append((i + offset, j + offset))

    return Motif(local_nodes=new_nodes, edges=new_edges)



