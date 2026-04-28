import numpy as np
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
event_index = 0
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

kx_end = root["track_vertex"]["Kplus"]["ORIVX_X"]
ky_end = root["track_vertex"]["Kplus"]["ORIVX_Y"]
kz_end = root["track_vertex"]["Kplus"]["ORIVX_Z"]

kx = kx_end[event_index]
ky = ky_end[event_index]
kz = kz_end[event_index]

k_vertex = go.Scatter3d(
                    x= [kx],
                    y= [ky],
                    z= [kz],
                    mode="markers",
                    name="K+ origin vertex",
                    marker={
                        "size": 6,
                        "color": PARTICLE_COLORS["Kplus"],
                    },
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
figure = go.Figure(data=[bplus_vertex, j_psi_vertex, j_psi_flight, k_vertex])
figure.show()






