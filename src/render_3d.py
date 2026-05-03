
import plotly.graph_objects as go
import build_godot as godot
import plotly.io as pio

pio.renderers.default = "browser"
PARTICLE_COLORS = {
    "muplus": "red",
    "muminus": "blue",
    "Kplus": "green",
    "Bplus": "purple",
    "J_psi_1S": "orange",

}

def root_data():
    root = godot.get_root()
    return root

root = root_data()
TRACK_SCALE = 0.1

def build_event_traces(event_index):
    x_start = root["track_vertex"]["Bplus"]["OWNPV_X"]
    y_start = root["track_vertex"]["Bplus"]["OWNPV_Y"]
    z_start = root["track_vertex"]["Bplus"]["OWNPV_Z"]

    x_end = root["vertex_decay"]["Bplus"]["ENDVERTEX_X"]
    y_end = root["vertex_decay"]["Bplus"]["ENDVERTEX_Y"]
    z_end = root["vertex_decay"]["Bplus"]["ENDVERTEX_Z"]

    jx_end = root["vertex_decay"]["J_psi_1S"]["ENDVERTEX_X"]
    jy_end = root["vertex_decay"]["J_psi_1S"]["ENDVERTEX_Y"]
    jz_end = root["vertex_decay"]["J_psi_1S"]["ENDVERTEX_Z"]

    x = [x_start[event_index], x_end[event_index]]
    y = [y_start[event_index], y_end[event_index]]
    z = [z_start[event_index], z_end[event_index]]

    jx = [jx_end[event_index]]
    jy = [jy_end[event_index]]
    jz = [jz_end[event_index]]

    mumix = root["kinematics"]["muminus"]["PX"]
    mumiy = root["kinematics"]["muminus"]["PY"]
    mumiz = root["kinematics"]["muminus"]["PZ"]

    muplx = root["kinematics"]["muplus"]["PX"]
    muply = root["kinematics"]["muplus"]["PY"]
    muplz = root["kinematics"]["muplus"]["PZ"]

    kpx = root["kinematics"]["Kplus"]["PX"]
    kpy = root["kinematics"]["Kplus"]["PY"]
    kpz = root["kinematics"]["Kplus"]["PZ"]

    kx_start = x_end[event_index]
    ky_start = y_end[event_index]
    kz_start = z_end[event_index]

    kx_track_end = kx_start + kpx[event_index] * TRACK_SCALE
    ky_track_end = ky_start + kpy[event_index] * TRACK_SCALE
    kz_track_end = kz_start + kpz[event_index] * TRACK_SCALE

    kx = [kx_start, kx_track_end]
    ky = [ky_start, ky_track_end]
    kz = [kz_start, kz_track_end]

    mumix_start = jx_end[event_index]
    mumiy_start = jy_end[event_index]
    mumiz_start = jz_end[event_index]

    mumix_end = mumix_start + mumix[event_index] * TRACK_SCALE
    mumiy_end = mumiy_start + mumiy[event_index] * TRACK_SCALE
    mumiz_end = mumiz_start + mumiz[event_index] * TRACK_SCALE

    muplx_start = jx_end[event_index]
    muply_start = jy_end[event_index]
    muplz_start = jz_end[event_index]

    muplx_end = muplx_start + muplx[event_index] * TRACK_SCALE
    muply_end = muply_start + muply[event_index] * TRACK_SCALE
    muplz_end = muplz_start + muplz[event_index] * TRACK_SCALE

    muplusx = [muplx_start, muplx_end]
    muplusy = [muply_start, muply_end]
    muplusz = [muplz_start, muplz_end]

    muminusx = [mumix_start, mumix_end]
    muminusy = [mumiy_start, mumiy_end]
    muminusz = [mumiz_start, mumiz_end]

    muplus_track = go.Scatter3d(
                        x=muplusx,
                        y=muplusy,
                        z=muplusz,
                        mode="lines+markers",
                        name="mu+ track direction",
                        line={
                            "color": PARTICLE_COLORS["muplus"],
                            "width": 2,
                        },
                        marker={
                            "size": 6,
                            "color": PARTICLE_COLORS["muplus"]
                        }
    )

    muminus_track = go.Scatter3d(
                        x=muminusx,
                        y=muminusy,
                        z=muminusz,
                        mode="lines+markers",
                        name="mu- track direction",
                        line={
                            "color": PARTICLE_COLORS["muminus"],
                            "width": 2,
                        },
                        marker={
                            "size": 6,
                            "color": PARTICLE_COLORS["muminus"]
                        }
    )

    k_track = go.Scatter3d(
                        x= kx,
                        y= ky,
                        z= kz,
                        mode="lines+markers",
                        name="K+ track direction",
                        line={
                            "color": PARTICLE_COLORS["Kplus"],
                            "width": 2,
                        },
                        marker={
                            "size": 6,
                            "color": PARTICLE_COLORS["Kplus"]
                        }
    )

    j_psi_flight = go.Scatter3d(
                        x=[x[1], jx[0]],
                        y=[y[1], jy[0]],
                        z=[z[1], jz[0]],
                        mode="lines+markers",
                        name="J/psi flight path",
                        line={
                            "color": PARTICLE_COLORS["J_psi_1S"],
                            "width": 2,
                        },
    )

    j_psi_vertex = go.Scatter3d(
                        x=jx,
                        y=jy,
                        z=jz,
                        mode="markers",
                        name="J/psi decay vertex",
                        marker={
                            "size": 6,
                            "color": PARTICLE_COLORS["J_psi_1S"],
                        },
    )

    bplus_vertex = go.Scatter3d(
                        x=x,
                        y=y,
                        z=z,
                        mode="lines+markers",
                        name="Bplus flight path",
                        line={
                            "color": PARTICLE_COLORS["Bplus"],
                            "width": 4,
                        },
                        marker={
                            "size": 8,
                            "color": PARTICLE_COLORS["Bplus"],
                        }
                    )
    return [bplus_vertex, j_psi_vertex, j_psi_flight, k_track, muplus_track, muminus_track]

all_traces = []

for event_index in range(1000):
    all_traces.extend(build_event_traces(event_index))




figure = go.Figure(data=all_traces)
figure.show()




