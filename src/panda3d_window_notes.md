dddddd# Panda3D Window Notes

These notes are for learning the syntax you are likely to need when making a
Panda3D window class. This is not a finished template. The point is to give you
the pieces, then let you decide where they belong in your own file.

## Window Syntax

Panda3D window programs usually start with `ShowBase`.

```python
from direct.showbase.ShowBase import ShowBase
```

The common class shape is:

```python
class MyWindow(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
```

Meaning:

- `MyWindow` is your own window/app class.
- `ShowBase` is Panda3D's base application class.
- `ShowBase.__init__(self)` opens the window and sets up Panda3D systems.

To start Panda3D's main loop, you eventually call:

```python
app.run()
```

That should happen once, usually after you create your app object.

## Window Settings

Some window settings can be configured before the window opens.

```python
from panda3d.core import loadPrcFileData
```

Common examples:

```python
loadPrcFileData("", "window-title My Panda3D Window")
loadPrcFileData("", "win-size 1280 720")
loadPrcFileData("", "show-frame-rate-meter true")
```

Important idea:

- These settings should appear before `ShowBase.__init__(self)` runs.
- If you put them after the window is already created, they may not affect the
  first window.

## Scene Graph

Panda3D uses a scene graph. You attach visible things into the scene graph so
the camera can see them.

The default 3D scene root is:

```python
self.render
```

You can make your own organizing node:

```python
self.scene_root = self.render.attachNewNode("scene-root")
```

That gives you a parent node where you can put related models, lines, markers,
or particle visualizations.

## Loading Models

The basic model-loading syntax is:

```python
model = self.loader.loadModel("path/to/model")
model.reparentTo(self.render)
```

Or, if you made your own scene root:

```python
model.reparentTo(self.scene_root)
```

Common transform methods:

```python
model.setPos(x, y, z)
model.setScale(scale)
model.setHpr(heading, pitch, roll)
```

Notes:

- `setPos()` moves the model.
- `setScale()` resizes it.
- `setHpr()` rotates it.
- `reparentTo()` is what actually places the model into the scene graph.

## Camera

The default camera is:

```python
self.camera
```

Panda3D gives the camera default mouse controls. If you want to position the
camera yourself, disable those controls:

```python
self.disableMouse()
```

Then you can move and aim the camera:

```python
self.camera.setPos(0, -20, 8)
self.camera.lookAt(0, 0, 0)
```

Panda3D's coordinates are commonly used like this:

- X: left/right
- Y: forward/back
- Z: up/down

So a camera at `(0, -20, 8)` is behind the origin and above it, looking toward
the center.

## Background Color

You can set the window background color with:

```python
self.setBackgroundColor(red, green, blue, alpha)
```

Example values:

```python
self.setBackgroundColor(0.02, 0.02, 0.04, 1)
```

Color values usually go from `0` to `1`.

## Controls

Keyboard and mouse input can be connected with `accept()`.

```python
self.accept("escape", self.userExit)
self.accept("r", self.reset_camera)
self.accept("mouse1", self.handle_left_click)
```

The first argument is the event name.
The second argument is the method that should run when the event happens.

Example method shapes:

```python
def reset_camera(self):
    pass

def handle_left_click(self):
    pass
```

Useful event names:

```text
escape
r
space
arrow_left
arrow_right
mouse1
mouse1-up
mouse2
mouse3
```

## Mouse Position

Disabling camera mouse control does not disable the mouse itself.

To read the mouse position:

```python
if self.mouseWatcherNode.hasMouse():
    x = self.mouseWatcherNode.getMouseX()
    y = self.mouseWatcherNode.getMouseY()
```

The mouse coordinates are usually in a screen-like range rather than world
space. You usually need extra logic before using them as 3D positions.

## Frame Updates

Panda3D uses tasks for code that should run every frame.

Import the task status constants:

```python
from direct.task import Task
```

Add a task:

```python
self.taskMgr.add(self.update, "update")
```

The method shape:

```python
def update(self, task):
    return Task.cont
```

Meaning:

- `task` is passed in by Panda3D.
- `Task.cont` tells Panda3D to keep running this task next frame.
- Returning `Task.done` would stop the task.

To get time between frames:

```python
dt = globalClock.getDt()
```

That is useful for smooth motion:

```python
self.angle += dt
```

## Lights

Basic light imports:

```python
from panda3d.core import AmbientLight, DirectionalLight
```

Ambient light affects everything softly:

```python
ambient = AmbientLight("ambient")
ambient.setColor((0.25, 0.25, 0.25, 1))
ambient_node = self.render.attachNewNode(ambient)
self.render.setLight(ambient_node)
```

Directional light acts more like sunlight:

```python
sun = DirectionalLight("sun")
sun.setColor((0.9, 0.9, 0.8, 1))
sun_node = self.render.attachNewNode(sun)
sun_node.setHpr(-45, -45, 0)
self.render.setLight(sun_node)
```

## Drawing Simple Lines

Lines are useful for axes, particle paths, detector traces, or debugging.

```python
from panda3d.core import LineSegs
```

Basic line syntax:

```python
lines = LineSegs()
lines.setThickness(2)
lines.setColor(1, 0, 0, 1)
lines.moveTo(0, 0, 0)
lines.drawTo(5, 0, 0)
node = lines.create()
self.render.attachNewNode(node)
```

For particle data, a start-to-end line might eventually use:

```python
lines.moveTo(start_x, start_y, start_z)
lines.drawTo(end_x, end_y, end_z)
```

## Connecting To Particle Data

Your `Particle` objects currently have fields like:

```python
particle.name
particle.id
particle.momentum
particle.start
particle.end
particle.energy
particle.mass
```

The most relevant fields for drawing in Panda3D are probably:

```python
particle.start
particle.end
particle.momentum
```

Possible decisions you will need to make:

- Should `start` become a 3D position?
- Should `end` become another 3D position?
- Should `momentum` control a line direction?
- Do the physics values need to be scaled down before drawing?
- What should happen if `particle.end` is `None`?

Example thinking, not finished code:

```python
start = particle.start
end = particle.end

if end is not None:
    # draw a line from start to end
    pass
else:
    # draw only a marker at start
    pass
```

## Common Panda3D Attributes

Inside a `ShowBase` subclass, these are commonly available:

```python
self.render
self.camera
self.loader
self.taskMgr
self.mouseWatcherNode
```

What they are for:

- `self.render`: main 3D scene root.
- `self.camera`: default camera.
- `self.loader`: loads models and other assets.
- `self.taskMgr`: manages frame-update tasks.
- `self.mouseWatcherNode`: reads mouse position and button state.

## Mental Checklist

When building your own Panda3D window file, ask:

1. Did I import `ShowBase`?
2. Did my class inherit from `ShowBase`?
3. Did I call `ShowBase.__init__(self)` inside `__init__`?
4. Did I attach visible things to `render` or a child of `render`?
5. Did I position the camera so it can see the scene?
6. Did I call `run()` once at the end?
7. If using particle data, did I handle missing values like `end = None`?
