#Various imports necessary for this game.
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


#Start of the game class, which is a subclass of ShowBase.
class Game(ShowBase):
    #Init method setting up ShowBase and the meat of the game
    def __init__(self):
        ShowBase.__init__(self)

        properties = WindowProperties()
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)
        self.disableMouse()

        #Load in the environment and actor
        self.environ = loader.loadModel("resources/PandaSampleModels-master/Environment/environment")
        self.environ.reparentTo(render)

        self.tempActor = Actor("resources/p3d_samples-master/models/act_p3d_chan", {"walk" : "resources/p3d_samples-master/models/a_p3d_chan_run"})
        self.tempActor.reparentTo(render)

        #Set ambient light
        ambientLight = AmbientLight("ambient light")
        ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.ambientLightNodePath = render.attachNewNode(ambientLight)
        render.setLight(self.ambientLightNodePath)

        #Set directional light
        mainLight = DirectionalLight("main light")
        self.mainLightNodePath = render.attachNewNode(mainLight)
        #Turn the light around by 45 degrees, and tilt it down by 45 degrees.
        self.mainLightNodePath.setHpr(45, -45, 0)
        render.setLight(self.mainLightNodePath)
        #Applying a shader that is automatically generated via the setShaderAuto method.
        render.setShaderAuto()
        
        #Move the camera to a position high above the screen
        #that is, offset it along the z-axis.
        self.camera.setPos(0, 0, 32)
        #Tilt the camera down by setting its pitch.
        self.camera.setP(-90)

        self.tempActor.getChild(0).setH(180)
        self.tempActor.loop("walk")
        
        #User input dictionary
        self.userInput = {
            "up" : False,
            "down" : False,
            "left" : False,
            "right" : False,
            "shoot" : False
        }

        #Tells panda what to do when certain keys are pressed
        self.accept("w", self.updateUserInput, ["up", True])
        self.accept("w-up", self.updateUserInput, ["up", False])
        self.accept("s", self.updateUserInput, ["down", True])
        self.accept("s-up", self.updateUserInput, ["down", False])
        self.accept("a", self.updateUserInput, ["left", True])
        self.accept("a-up", self.updateUserInput, ["left", False])
        self.accept("d", self.updateUserInput, ["right", True])
        self.accept("d-up", self.updateUserInput, ["right", False])
        self.accept("mouse1", self.updateUserInput, ["shoot", True])
        self.accept("mouse1-up", self.updateUserInput, ["shoot", False])

        #Use task-manager to run an update loop
        self.updateTask = taskMgr.add(self.update, "update")

        #A pusher prevents solid objects from intersecting other solids
        self.pusher = CollisionHandlerPusher()
        #Call the default variable cTrav to have panda update that traverser
        self.cTrav = CollisionTraverser()

        self.pusher.setHorizontal(True)

        colliderNode = CollisionNode("player")
        #Add a collision-sphere centered on (0,0,0), and with a radius of 0.3
        colliderNode.addSolid(CollisionSphere(0, 0, 0, 0.3))
        collider = self.tempActor.attachNewNode(colliderNode)

        # The pusher wants a collider, and a NodePath that
        # should be moved by that collider's collisions.
        # In this case, we want the player-Actor to be moved.
        base.pusher.addCollider(collider, self.tempActor)
        # The traverser wants a collider, and a handler
        # that responds to that collider's collisions
        base.cTrav.addCollider(collider, self.pusher)

        
        # Tubes are defined by their start-points, end-points, and radius.
        # In this first case, the tube goes from (-8, 0, 0) to (8, 0, 0),
        # and has a radius of 0.2.
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

        
    def updateUserInput(self, controlName, controlState):
        self.userInput[controlName] = controlState


    #Method to update the task again if need-be
    def update(self, task):
        # Get the amount of time since the last update
        dt = globalClock.getDt()

        # If any movement keys are pressed, use the above time
        # to calculate how far to move the character, and apply that.
        if self.userInput["up"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(0, 5.0*dt, 0))
        if self.userInput["down"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(0, -5.0*dt, 0))
        if self.userInput["left"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(-5.0*dt, 0, 0))
        if self.userInput["right"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(5.0*dt, 0, 0))
        if self.userInput["shoot"]:
            print ("Zap!")

        return task.cont
        
          
game = Game()
game.run()
