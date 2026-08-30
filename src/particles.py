import build_godot as gd

def root_data():
    return gd.get_root()

class Particle:
    def __init__(self, root, name):
        self.root = root
        self.name = name
        self.id = None
        self.p = None
        self.px = None
        self.py = None
        self.pz = None
        self.pt = None
        self.mass = None
        self.energy = None
        self.start = None
        self.end = None
        self.momentum = None



    def load_id(self):
        self.id = self.root["identity"][self.name]["ID"]


    def load_momentum(self):
        self.px = self.root["kinematics"][self.name]["PX"]
        self.py = self.root["kinematics"][self.name]["PY"]
        self.pz = self.root["kinematics"][self.name]["PZ"]

        self.momentum = [self.px, self.py, self.pz]


    def load_kinematics(self):
        self.p = self.root["kinematics"][self.name]["P"]
        self.pt = self.root["kinematics"][self.name]["PT"]
        self.mass = self.root["kinematics"][self.name]["M"]
        self.energy = self.root["kinematics"][self.name]["PE"]

    def load_start(self):
        self.start = [
        self.root["track_vertex"][self.name]["OWNPV_X"],
        self.root["track_vertex"][self.name]["OWNPV_Y"],
        self.root["track_vertex"][self.name]["OWNPV_Z"],
        ]

    def load_end(self):
        if self.name not in self.root["vertex_decay"]:
            self.end = None
            return

        vertex_decay = self.root["vertex_decay"][self.name]

        end_x = vertex_decay["ENDVERTEX_X"]
        end_y = vertex_decay["ENDVERTEX_Y"]
        end_z = vertex_decay["ENDVERTEX_Z"]

        if end_x is None or end_y is None or end_z is None:
            self.end = None
            return

        self.end = [
            end_x,
            end_y,
            end_z,
        ]



    def blueprint(self):
        self.load_id()
        self.load_momentum()
        self.load_kinematics()
        self.load_start()
        self.load_end()
        return self



    def __str__(self):
        return (
            f"Particle: {self.name}\n"
            f"ID: {self.id}\n"
            f"Momentum: {self.momentum}\n"
            f"P: {self.p}\n"
            f"PT: {self.pt}\n"
            f"Mass: {self.mass}\n"
            f"Energy: {self.energy}\n"
            f"Start: {self.start}\n"
            f"End: {self.end}"
        )



def get_particles():
    root = root_data()
    muplus = Particle(root, 'muplus').blueprint()
    muminus = Particle(root, 'muminus').blueprint()
    bplus = Particle(root, 'Bplus').blueprint()
    kplus = Particle(root, 'Kplus').blueprint()
    jpsi = Particle(root, 'J_psi_1S').blueprint()

    return muplus, muminus, bplus, kplus, jpsi


if __name__ == '__main__':
    get_particles()








