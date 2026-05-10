
import plotly.graph_objects as go
import build_godot as godot
import plotly.io as pio
import math

pio.renderers.default = "browser"
PARTICLE_COLORS = {
    "muplus": "red",
    "muminus": "blue",
    "Kplus": "green",
    "Bplus": "purple",
    "J_psi_1S": "orange",

}

PDG_CHARGES = {
    13: -1,
    -13: 1,
    321: 1,
    -321: -1,
    521: 1,
    443: 0,
}

PARTICLES = {
    "muplus": {
        "kinematics": {
            "category": "kinematics",
            "particle": "muplus",
            "px": "PX",
            "py": "PY",
            "pz": "PZ",
            "p": "P",
            "pt": "PT",
            "energy": "PE",
            "mass": "M",
        },
        "start": {
            "category": "vertex_decay",
            "particle": "J_psi_1S",
            "x": "ENDVERTEX_X",
            "y": "ENDVERTEX_Y",
            "z": "ENDVERTEX_Z",
        },
        "identity":{
            "category": "identity",
            "particle": "muplus",
            "id": "ID",
        },
    },

    "muminus": {
        "kinematics": {
            "category": "kinematics",
            "particle": "muminus",
            "px": "PX",
            "py": "PY",
            "pz": "PZ",
            "p": "P",
            "pt": "PT",
            "energy": "PE",
            "mass": "M",
            },
        "start": {
            "category": "vertex_decay",
            "particle": "J_psi_1S",
            "x": "ENDVERTEX_X",
            "y": "ENDVERTEX_Y",
            "z": "ENDVERTEX_Z",
            },
        "identity":{
            "category": "identity",
            "particle": "muminus",
            "id": "ID",
            },
        },
    "Bplus": {
        "track_vertex": {
            "category": "track_vertex",
            "particle": "Bplus",
        },
        "kinematics": {
            "category": "kinematics",
            "particle": "Bplus",
            "px": "PX",
            "py": "PY",
            "pz": "PZ",
            "p": "P",
            "pt": "PT",
            "energy": "PE",
            "mass": "M",
        },
        "start": {
            "category": "track_vertex",
            "particle": "Bplus",
            "x": "OWNPV_X",
            "y": "OWNPV_Y",
            "z": "OWNPV_Z",
        },
        "end": {
            "category": "vertex_decay",
            "particle": "Bplus",
            "x": "ENDVERTEX_X",
            "y": "ENDVERTEX_Y",
            "z": "ENDVERTEX_Z",
        },
        "identity": {
            "category": "vertex_decay",
            "particle": "Bplus",
            "id": "ID",
        }
    },
    "J_psi_1S": {
        "vertex_decay": {
            "category": "vertex_decay",
            "particle": "J_psi_1S",
        },
        "kinematics": {
            "category": "kinematics",
            "particle": "J_psi_1S",
            "px": "PX",
            "py": "PY",
            "pz": "PZ",
            "p": "P",
            "pt": "PT",
            "energy": "PE",
            "mass": "M",
        },
        "start": {
            "category": "vertex_decay",
            "particle": "Bplus",
            "x": "ENDVERTEX_X",
            "y": "ENDVERTEX_Y",
            "z": "ENDVERTEX_Z",
        },
        "end": {
            "category": "vertex_decay",
            "particle": "J_psi_1S",
            "x": "ENDVERTEX_X",
            "y": "ENDVERTEX_Y",
            "z": "ENDVERTEX_Z",
        },
        "identity": {
            "category": "vertex_decay",
            "particle": "J_psi_1S",
            "id": "ID",
        }
    },
    "Kplus": {
        "kinematics": {
            "category": "kinematics",
            "particle": "Kplus",
            "px": "PX",
            "py": "PY",
            "pz": "PZ",
            "p": "P",
            "pt": "PT",
            "energy": "PE",
            "mass": "M",
        },
        "start": {
            "category": "vertex_decay",
            "particle": "Bplus",
            "x": "ENDVERTEX_X",
            "y": "ENDVERTEX_Y",
            "z": "ENDVERTEX_Z",
        },
        "identity": {
            "category": "identity",
            "particle": "Kplus",
            "id": "ID",
        }
    }
}
def clamp(value, minimum=0.0, maximum=1.0):
    return max(maximum, min(value, maximum))

def get_charge(pdg_id, default=0):
    try:
        return PDG_CHARGES.get(int(pdg_id), default)

    except (TypeError, ValueError):
        return default

def calculate_curvature(charge, momentum, curvature_scale=10000.0):
    if charge == 0 or momentum == 0:
        return 0.0
    curvature_amount = curvature_scale / abs(momentum)
    curvature_amount = clamp(curvature_amount, 0.02, 0.75)

    return charge * curvature_amount

def get_particle_id(particle_config, event_index):
    identity = particle_config.get("identity")

    if identity is None:
        return 0

    return get_value(
        {
            **identity,
            "field": identity["id"],
        },
        event_index,
        default=0.0,
    )

def get_value(config, event_index, default=0.0):
    category = config["category"]
    particle = config["particle"]
    field = config["field"]

    value = root.get(category,{}).get(particle, {}).get(field)

    if value is None:
        return default

    try:
        return float(value[event_index])
    except (IndexError, TypeError, ValueError):
        return default

def get_point(point_config, event_index):
    x = get_value({**point_config, "field": point_config["x"]}, event_index)
    y = get_value({**point_config, "field": point_config["y"]}, event_index)
    z = get_value({**point_config, "field": point_config["z"]}, event_index)

    return x, y, z

def get_kinematics(particle_config, event_index):
    kinematics = particle_config["kinematics"]

    return {
        "px": get_value({**kinematics, "field": kinematics["px"]}, event_index),
        "py": get_value({**kinematics, "field": kinematics["py"]}, event_index),
        "pz": get_value({**kinematics, "field": kinematics["pz"]}, event_index),
        "p": get_value({**kinematics, "field": kinematics["p"]}, event_index),
        "pt": get_value({**kinematics, "field": kinematics["pt"]}, event_index),
        "energy": get_value({**kinematics, "field": kinematics["energy"]}, event_index),
        "mass": get_value({**kinematics, "field": kinematics["mass"]}, event_index)
    }

def build_vertex_to_vertex_trace(particle_name, particle_config, event_index):
    start_x, start_y, start_z = get_point(particle_config["start"], event_index)
    end_x, end_y, end_z = get_point(particle_config["end"], event_index)

    return go.Scatter3d(
        x=[start_x, end_x],
        y=[start_y, end_y],
        z=[start_z, end_z],
        mode="lines+markers",
        name=f"{particle_name} flight path",
        line={
            "color": PARTICLE_COLORS[particle_name],
            "width": 4,
        },
        marker={
            "size": 8,
            "color": PARTICLE_COLORS[particle_name]
        }
    )

def build_curved_track(start_x, start_y, start_z, end_x, end_y, end_z, curvature, steps=16):
    if curvature == 0:
        return [start_x, end_x], [start_y, end_y], [start_z, end_z]

    xs = []
    ys = []
    zs = []

    for step in range(steps + 1):
        t = step / steps

        x = start_x + (end_x - start_x) * t
        y = start_y + (end_y - start_y) * t
        z = start_z + (end_z - start_z) * t

        curve_offset = math.sin(t * math.pi) * curvature * 200.0

        x += curve_offset
        y += curve_offset * 0.5

        xs.append(x)
        ys.append(y)
        zs.append(z)
    return xs, ys, zs

def build_momentum_trace(particle_name, particle_config, event_index):
    start_x, start_y, start_z = get_point(particle_config["start"], event_index)
    kinematics = get_kinematics(particle_config, event_index)

    pdg_id = get_particle_id(particle_config, event_index)
    charge = get_charge(pdg_id)
    curvature = calculate_curvature(charge, kinematics["p"])

    end_x = start_x + kinematics["px"] * TRACK_SCALE
    end_y = start_y + kinematics["py"] * TRACK_SCALE
    end_z = start_z + kinematics["pz"] * TRACK_SCALE

    x_points, y_points, z_points = build_curved_track(
        start_x,
        start_y,
        start_z,
        end_x,
        end_y,
        end_z,
        curvature,
    )

    return go.Scatter3d(
        x=x_points,
        y=y_points,
        z=z_points,
        mode="lines+markers",
        name=(
            f'{particle_name} momentum track | '
            f'ID={int(pdg_id)} | charge={charge} | curvature={curvature:.4f}'
        ),
        line={
            "color": PARTICLE_COLORS[particle_name],
            "width": 2,
        },
        marker={
            "color": PARTICLE_COLORS[particle_name],
            "size": 6,
        },
    )


def root_data():
    root = godot.get_root()
    return root

root = root_data()
TRACK_SCALE = 0.1

def build_event_traces(event_index):
    traces = []

    for particle_name, particle_config in PARTICLES.items():
       if "end" in particle_config:
           trace = build_vertex_to_vertex_trace(
               particle_name,
               particle_config,
               event_index,
           )
       else:
           trace = build_momentum_trace(
               particle_name,
               particle_config,
               event_index,
           )
       traces.append(trace)
    return traces

all_traces = []
for event_index in range(1000):
    all_traces.extend(build_event_traces(event_index))


figure = go.Figure(data=all_traces)
figure.show()



'''
TO ADD:
This is a bigger but clean upgrade to render_3d.py. It keeps your current idea, but adds:
particle loop
charge lookup
hover data
optional curved tracks
line width from intensity
marker size from mass
event title
B+ / B- classification

get_value()
calculate_momentum()
normalize_vector()
get_charge_from_pdg_id()
calculate_vfx_curvature()
build_particle_hover()
build_track_trace()

Data types to be added:
intensity
mass/weight
momentum/speed
charge/polarity
ghost/transparency
focus/scatter
curvature approximation
B+ vs B- variant
particle ID labels
'''
