# coding=utf-8
__author__ = "Vicente Guzmán Pinto"
__license__ = "MIT"

## Imports
# Libraries imports
from msilib.schema import Class
from OpenGL.GL import *
import random
import glfw
from typing import List
import sys, os.path
import numpy as np

# Local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.easy_shaders as es
import grafica.performance_monitor as pm
from grafica.assets_path import getAssetPath

# Sets the value to win
N = sys.argv[1] 

# Tool that counts time passed and its fps
perfMon = pm.PerformanceMonitor(glfw.get_time(),1.5)

# Settings to create shapes
def create_gpu(shape, pipeline):
    gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpu)
    gpu.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpu

# Class that represents a Flappy Bird
class Bird(object):

   #Initializes on the program
   def __init__(self, pipeline):

      # Creates the bird shape
      gpu_bird = create_gpu(bs.createColorQuad(1,1,0), pipeline)
      bird = sg.SceneGraphNode('bird')
      bird.transform = tr.matmul([tr.uniformScale(0.2), tr.translate(-2.5, 0, 0)]) 
      bird.childs += [gpu_bird]

      self.model = bird
      self.y = 0  # Indicates visual position of bird
      self.alive = True # Indicates if the bird is alive or not
      self.velocity = np.array([0, 0, 0], dtype=np.float32)

   # Draws the shape into the scene
   def draw(self, pipeline):
     sg.drawSceneGraphNode(self.model, pipeline, 'transform')

   # Transforms the model geometry according to interns variables 
   def modifymodel(self):
      self.model.transform = tr.matmul([tr.uniformScale(0.2), tr.translate(-2.5, self.y, 0)])

   # Updates the position of the bird
   def updatePosition(self, gravity, dt):
      self.velocity += dt * gravity
      self.y += self.velocity[1] 
      self.modifymodel()

   # Lets bird moves up
   def up(self):
      if not self.alive:
         return
      self.velocity = 0.0029

   #Shows if it collides with a tube
   def collide(self, tubes: 'TubeFactory'):
      range = 0.075 # rango que hay entre el centro de la separación de las tuberías y las tuberías
      if not tubes.on:  # Si el jugador perdió, no detecta colisiones
         return

      #Erase tubes that was surpassed and kill bird if it collides
      deleted_tubes = []
      for e in tubes.tubes:
         if e.pos_x < -1.3:
            self.counter(tubes)
            deleted_tubes.append(e)
         elif -1 <= e.pos_x <= -0.57 and not(self.y/10 - range <= e.pos_y/2 <= self.y/10 + range):
            tubes.die()
            self.alive = False
      tubes.delete(deleted_tubes)

   # Counts the amount of tubes that the player surpasses
   def counter(self, tubes: 'TubeFactory'):
      tubes.count += 1
      if tubes.count >= int(N):
         tubes.win()

# Class that represents a tube
class Tube(object):

   #Initializes on the program
   def __init__(self, pipeline):

      # Creates the tube shape
      gpu_tube = create_gpu(bs.createColorQuad(0,1,0), pipeline)

      # Tube model
      tube = sg.SceneGraphNode('tube')
      tube.transform = tr.scale(0.3, 1.5, 1)
      tube.childs += [gpu_tube]

      # Superior tube
      tube_sup = sg.SceneGraphNode('tubeSup')
      tube_sup.transform = tr.translate(0.3, 1.0, 0)
      tube_sup.childs = [tube]

      # Inferior tube
      tube_inf = sg.SceneGraphNode('tubeInf')
      tube_inf.transform = tr.translate(0.3, -1.0, 0)
      tube_inf.childs = [tube]

      # Tubes column
      tube_tr = sg.SceneGraphNode('tubeTR')
      tube_tr.childs += [tube_sup, tube_inf]

      self.pos_x = 1
      self.pos_y = (random.randrange(-55 , 55, 1))/100
      self.model = tube_tr

   # Draws the shape into the scene
   def draw(self, pipeline):
      self.model.transform = tr.translate(self.pos_x, self.pos_y, 0)
      sg.drawSceneGraphNode(self.model, pipeline, "transform")

   # Updates the position of a tube
   def updatePosition(self, dt):
      self.pos_x -= dt

# Class that represents a factory who makes tubes
class TubeFactory(object):
   tubes: List['Tube']
   count = 0

   #Initializes on the program
   def __init__(self):
      self.tubes = []
      self.on = True

   # Sets the scene when the player dies
   def die(self):
      glClearColor(1, 0, 0, 1.0)  # Cambiamos a rojo
      self.on = False  # Dejamos de generar tuberías, si es True es porque el jugador ya perdió

   # Sets the scene when the player wins
   def win(self):
      glClearColor(0, 0.4, 0, 1.0)  # Cambiamos a verde

   # Factory that creates tubes in the scene
   def create_tube(self, pipeline):
      perfMon.update(glfw.get_time())

      if len(self.tubes) >= 10 or not self.on:  # No puede haber más de 10 tuberías en pantalla
         return
      if (perfMon.period + perfMon.getDeltaTime()) > perfMon.getTimer() > (perfMon.period - perfMon.getDeltaTime()): #Creates a tube every period selected in line 26
         self.tubes.append(Tube(pipeline))

   # Draws the shape into the scene
   def draw(self, pipeline):
      for k in self.tubes:
         k.draw(pipeline)

   # Updates the position of tubes
   def updatePosition(self, dt):
      for k in self.tubes:
         k.updatePosition(dt)

   # Deletes tubes in list
   def delete(self, d):
      if len(d) == 0:
         return
      remain_tubes = []
      for k in self.tubes:  # Recorro todas las tuberías
         if k not in d:  # Si no se elimina, lo añado a la lista de tuberías que quedan
            remain_tubes.append(k)
      self.tubes = remain_tubes  # Actualizo la lista