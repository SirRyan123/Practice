from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from direct.actor.Actor import Actor
from panda3d.core import AmbientLight
from panda3d.core import Vec4, Vec3
from panda3d.core import DirectionalLight
from panda3d.core import CollisionTraverser
from panda3d.core import CollisionHandlerPusher
from panda3d.core import CollisionSphere, CollisionNode
from panda3d.core import CollisionTube
from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from GameObject import *


class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        #window properties
        properties = WindowProperties()
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)
        self.disableMouse()

        self.environ = loader.loadModel("/c/Users/ryand/Desktop/VSCode_Workspace/Panda3D Practice/Game/Models/environment")
        self.environ.reparentTo(render)

        #place camera high above the ground (z axis)
        self.camera.setPos(0, 0, 32)
        #set pitch to look down (camera points straight by default)
        self.camera.setP(-90)

        #ambient light (light for entire scene)
        ambientLight = AmbientLight("ambient light")
        ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.ambientLightNodePath = render.attachNewNode(ambientLight)
        #use render.setLight to make the light affect the entire scene
        render.setLight(self.ambientLightNodePath)

        #directional light (shading)
        directLight = DirectionalLight("direct light")
        self.directLightNodePath = render.attachNewNode(directLight)
        self.directLightNodePath.setHpr(-45,-45,0)
        render.setLight(self.directLightNodePath)
        #use pandas built in shader generator
        render.setShaderAuto()


        self.keyMap = {
            "up" : False,
            "down" : False,
            "left" : False,
            "right" : False,
            "shoot" : False
        }

        self.accept("w", self.updateKeyMap, ["up", True])
        self.accept("w-up", self.updateKeyMap, ["up", False])
        self.accept("s", self.updateKeyMap, ["down", True])
        self.accept("s-up", self.updateKeyMap, ["down", False])
        self.accept("a", self.updateKeyMap, ["left", True])
        self.accept("a-up", self.updateKeyMap, ["left", False])
        self.accept("d", self.updateKeyMap, ["right", True])
        self.accept("d-up", self.updateKeyMap, ["right", False])
        self.accept("mouse1", self.updateKeyMap, ["shoot", True])
        self.accept("mouse1-up", self.updateKeyMap, ["shoot", False])

        self.updateTask = taskMgr.add(self.update, "update")
        
        #panda will automatically update the travserser with this cTrav variable
        self.cTrav = CollisionTraverser()
        #we want to add and remove objects as called for, so add this
        self.pusher = CollisionHandlerPusher()
        #because its a 2d game
        self.pusher.setHorizontal(True)

        wallSolid = CollisionTube(-8.0, 0, 0, 8.0, 0, 0, 0.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)

        wallSolid = CollisionTube(-8.0, 0, 0, 8.0, 0, 0, 0.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(-8.0)

        wallSolid = CollisionTube(0, -8.0, 0, 0, 8.0, 0, 0.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setX(8.0)

        wallSolid = CollisionTube(0, -8.0, 0, 0, 8.0, 0, 0.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setX(-8.0)
        
        #instantiate a player instance and walking enemy instance
        self.player = Player()
        self.tempEnemy = WalkingEnemy(Vec3(5, 0, 0))

        #starter code for button controls
        self.bk_text = "Test Button"
        self.textObject = OnscreenText(text=self.bk_text, pos=(0.95,-0.95), scale=0.07,
                                    fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter, mayChange=1)

        self.button = DirectButton(text=("OK", "click!", "rolling over", "disabled"), scale=.1, command=self.setText)


    def updateKeyMap(self, ctrlName, ctrlState):
        self.keyMap[ctrlName] = ctrlState
        print(ctrlName, "set to", ctrlState)


    def update(self, task):
        #get time since last update (helps with fps issues)
        dt = globalClock.getDt()

        self.player.update(self.keyMap, dt)
        self.tempEnemy.update(self.player, dt)

        return task.cont


    #sets text when button is pressed
    def setText(self):
        self.bk_text = "Button Clicked"
        self.textObject.setText(self.bk_text)
        



#run the class
game = MyGame()
game.run()