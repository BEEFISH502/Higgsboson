from panda3d.core import loadPrcFileData
from direct.showbase.ShowBase import ShowBase
from particles import get_particles
from panda3d.core import AmbientLight

loadPrcFileData("", "window-title Collider")
loadPrcFileData("", "win-size 1280 720")
loadPrcFileData("", "show-frame-rate-meter true")
loadPrcFileData("", "fullscreen true")

muplus, muminus, bplus, kplus, jpsi = get_particles()

class GameWindow(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.accept("escape", self.exit_game)
        self.setBackgroundColor(0, 0, 0, 1)
        self.ambient_light()
        self.render_particles()


    def ambient_light(self):
        ambient = AmbientLight("ambient")
        ambient.setColor((1, 1, 1, 1))
        ambient_node = self.render.attachNewNode(ambient)
        self.render.setLight(ambient_node)

    def exit_game(self):
        self.userExit()

    def render_particles(self):
        x = bplus.start[0]
        y = bplus.start[1]
        z = bplus.start[2]

        for i in range(1000):
            sphere = self.loader.loadModel("models/misc/sphere")
            sphere.reparentTo(self.render)
            sphere.setPos(x[i], y[i], z[i])
            sphere.setScale(0.2)


def main():
    game = GameWindow()
    game.run()

if __name__ == '__main__':
    main()

