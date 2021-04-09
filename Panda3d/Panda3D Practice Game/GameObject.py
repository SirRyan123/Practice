from panda3d.core import Vec3, Vec2
from direct.actor.Actor import Actor
from panda3d.core import CollisionSphere, CollisionNode

FRICTION = 150.0

class GameObject():
    def __init__(self, pos, modelName, modelAnims, maxHP, maxSpeed, colliderName):
        self.actor = Actor(modelName, modelAnims)
        self.actor.reparentTo(render)
        self.actor.setPos(pos)

        self.maxHP = maxHP
        self.health = maxHP

        self.maxSpeed = maxSpeed

        self.velocity = Vec3(0, 0, 0)
        self.acceleration = 300.0

        self.walking = False

        colliderNode = CollisionNode(colliderName)
        colliderNode.addSolid(CollisionSphere(0, 0, 0, 0.3))
        self.collider = self.actor.attachNewNode(colliderNode)
        self.collider.setPythonTag("owner", self)


    def update(self, dt):
        #if going faster than max speed,
        #set velocity-vector length to match that current speed
        speed = self.velocity.length()
        if speed > self.maxSpeed:
            self.velocity.normalize()
            self.velocity = self.velocity * self.maxSpeed
            speed = self.maxSpeed

        #if walking, dont worry about friction
        #otherwise, use friction to slow player down
        if not self.walking:
            frictionVal = FRICTION * dt
            if frictionVal > speed:
                self.velocity.set(0, 0, 0)
            else:
                frictionVec = -self.velocity
                frictionVec.normalize()
                frictionVec = frictionVec * frictionVal

                self.velocity = self.velocity + frictionVec


        #move the character using current velocity multiplied by the time since last update
        self.actor.setPos(self.actor.getPos() + self.velocity * dt)

    
    def alterHealth(self, dHealth):
        self.health = self.health + dHealth

        if self.health > self.maxHP:
            self.health = self.maxHP


    def cleanup(self):
        if self.collider is not None and not self.collider.isEmpty():
            self.collider.clearPythonTag("owner")
            base.cTrav.removeCollider(self.collider)
            base.pusher.removeCollider(self.collider)

        if self.actor is not None:
            self.actor.cleanup()
            self.actor.removeNode()
            self.actor = None

        self.collider = None


class Player(GameObject):
    def __init__(self):
        GameObject.__init__(self,
                        Vec3(0, 0, 0),
                        "/c/Users/ryand/Desktop/VSCode_Workspace/Panda3D Practice/Game/Models/act_p3d_chan",
                        {
                            "stand" : "/c/Users/ryand/Desktop/VSCode_Workspace/Panda3D Practice/Game/Models/a_p3d_chan_idle",
                            "walk" : "/c/Users/ryand/Desktop/VSCode_Workspace/Panda3D Practice/Game/Models/a_p3d_chan_run"
                        },
                        5,
                        10,
                        "player")
        
        #make actor face forwards instead of backwards (turning first sub-node)
        self.actor.getChild(0).setH(180)

        #since our game objects are ShowBase objects, we can access it via the
        #global base variable
        base.pusher.addCollider(self.collider, self.actor)
        base.cTrav.addCollider(self.collider, base.pusher)

        self.actor.loop("stand")


    def update(self, keys, dt):
        GameObject.update(self, dt)

        self.walking = False

        if keys["up"]:
            self.walking = True
            self.velocity.addY(self.acceleration * dt)
        if keys["down"]:
            self.walking = True
            self.velocity.addY(-self.acceleration * dt)
        if keys["left"]:
            self.walking = True
            self.velocity.addX(-self.acceleration * dt)
        if keys["right"]:
            self.walking = True
            self.velocity.addX(self.acceleration * dt)

        if self.walking:
            standControl = self.actor.getAnimControl("stand")
            if standControl.isPlaying():
                standControl.stop()

            walkControl = self.actor.getAnimControl("walk")
            if not walkControl.isPlaying():
                self.actor.loop("walk")
        else:
            standControl = self.actor.getAnimControl("stand")
            if not standControl.isPlaying():
                self.actor.stop("walk")
                self.actor.loop("stand")


class Enemy(GameObject):
    def __init__(self, pos, modelName, modelAnims, maxHP, maxSpeed, colliderName):
        GameObject.__init__(self, pos, modelName, modelAnims, maxHP, maxSpeed, colliderName)

        self.scoreValue = 1


    #update as a gameObject
    #run whatever enemy only logic is to be done
    def update(self, player, dt):
        GameObject.update(self, dt)

        self.runLogic(player, dt)

        #for the player, play the appropriate animation
        if self.walking:
            walkControl = self.actor.getAnimControl("walk")
            if not walkControl.isPlaying():
                self.actor.loop("walk")
        else:
            spawnControl = self.actor.getAnimControl("spawn")
            if spawnControl is None or not spawnControl.isPlaying():
                attackControl = self.actor.getAnimControl("attack")
                if attackControl is None or not attackControl.isPlaying():
                    standControl = self.actor.getAnimControl("stand")
                    if not standControl.isPlaying():
                        self.actor.loop("stand")


    #stub method
    def runLogic(self, player, dt):
        pass


class WalkingEnemy(Enemy):
    def __init__(self, pos):
        Enemy.__init__(self, pos, 
                      "/c/Users/ryand/Desktop/VSCode_Workspace/Panda3D Practice/Game/Models/SimpleEnemy/simpleEnemy",
                      {
                        "stand" : "/c/Users/ryand/Desktop/VSCode_Workspace/Panda3D Practice/Game/Models/SimpleEnemy/simpleEnemy-stand",
                        "walk" : "/c/Users/ryand/Desktop/VSCode_Workspace/Panda3D Practice/Game/Models/SimpleEnemy/simpleEnemy-walk",
                        "attack" : "/c/Users/ryand/Desktop/VSCode_Workspace/Panda3D Practice/Game/Models/SimpleEnemy/simpleEnemy-attack",
                        "die" : "/c/Users/ryand/Desktop/VSCode_Workspace/Panda3D Practice/Game/Models/SimpleEnemy/simpleEnemy-die",
                        "spawn" : "/c/Users/ryand/Desktop/VSCode_Workspace/Panda3D Practice/Game/Models/SimpleEnemy/simpleEnemy-spawn"
                      },
                      3.0,
                      7.0,
                      "walkingEnemy")
        
        self.attackDistance = 0.75
        self.acceleration = 100.0

        #reference vector to determine
        #which way to face the Actor
        #since character faces along
        #y direction, we use the y axis
        self.yVector = Vec2(0, 1)


    #find vector between enemy and player
    #if enemy is far from player, use vector to move toward player
    #otherwise, stop for now
    #finally, face the player using the heading
    def runLogic(self, player, dt):
        vectorToPlayer = player.actor.getPos() - self.actor.getPos()

        vectorToPlayer2D = vectorToPlayer.getXy()
        distanceToPlayer = vectorToPlayer2D.length()

        vectorToPlayer2D.normalize()

        heading = self.yVector.signedAngleDeg(vectorToPlayer2D)

        if distanceToPlayer > self.attackDistance * 0.9:
            self.walking = True
            vectorToPlayer.setZ(0)
            vectorToPlayer.normalize()
            self.velocity = (self.velocity + vectorToPlayer * self.acceleration * dt)
        else:
            self.walking = False
            self.velocity.set(0, 0, 0)

        self.actor.setH(heading)
