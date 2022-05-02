# coding=utf-8
__author__ = "Vicente Guzmán Pinto"
__license__ = "MIT"

## Imports
from model import Bird, TubeFactory
import glfw
import sys
from typing import Union

# Class that connects inputs and model
class Controller(object):
   model: Union['Bird', None]  # Con esto queremos decir que el tipo de modelo es 'Bird' (nuestra clase) ó None
   tubes: Union['TubeFactory', None]

   #Initializes on the program
   def __init__(self):
      self.model = None
      self.tubes = None

   # Defines and sets model
   def set_model(self, m):
      self.model = m

   #Defines and sets tubes
   def set_tubes(self, e):
      self.tubes = e
   
   # Interprets the inputs and modifies the model
   def on_key(self, window, key, scancode, action, mods):
      if action != glfw.PRESS:
         return

      # Esc: close game
      if key == glfw.KEY_ESCAPE:
         glfw.set_window_should_close(window, True)

      # UpArrow/SpaceBar: Bird flies
      elif key == glfw.KEY_UP or key == glfw.KEY_SPACE:
         self.model.up()
         print('Flap')

      # Any other button
      else:
         print('Press UpArrow or SpaceBar')