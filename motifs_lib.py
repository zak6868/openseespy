from motif import Motif

motifs = {}

motifs["square_2D"] = Motif(
    local_nodes=[(0,0,0),(1,0,0),(1,0,-1),(0,0,-1)],
    edges=[(0,1),(1,2),(2,3),(3,0)]
)

motifs["square_2D_diag1"] = Motif(
    local_nodes=[(0,0,0),(1,0,0),(1,0,-1),(0,0,-1)],
    edges=[(0,1),(1,2),(2,3),(3,0),(0,2)]
)

motifs["square_2D_diag2"] = Motif(
    local_nodes=[(0,0,0),(1,0,0),(1,0,-1),(0,0,-1)],
    edges=[(0,1),(1,2),(2,3),(3,0),(1,3)]
)

motifs["vertical_col"] = Motif(
    local_nodes=[(0,0,0),(0,0,-1)],
    edges=[(0,1)]
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
