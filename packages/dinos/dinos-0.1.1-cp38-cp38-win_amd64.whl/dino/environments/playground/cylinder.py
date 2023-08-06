import math
import random
import numpy as np
from scipy.spatial.distance import euclidean

import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
from pymunk import Vec2d
import pymunk.pygame_util

from panda3d.core import Point2, Point3, Vec2, Vec3, Vec4
from dino.environments.engines.tools.panda import PandaTools

from dino.representation.physical_entity import PhysicalEntity
from dino.representation.property import MethodObservable, AttributeObservable


class Cylinder(PhysicalEntity):
    def __init__(self, coords=(480, 300), radius=20, movable=True, name='', color=None, xydiscretization=20):
        super().__init__(self.__class__.__name__, name)
        self.coordsInit = coords
        self.coords = coords
        self.direction = 0.

        self.pandaInit = False

        self.radius = radius
        self.color = color if color else (
            (0, 224, 128) if movable else (255, 0, 0))
        self.mass = 1. if movable else 1000000.

        MethodObservable(self, 'position', self.absolutePosition,
                         discretization=xydiscretization)
        MethodObservable(self, 'positionToAgent', self.positionToAgent,
                         discretization=xydiscretization)  # .learnable = False
        
        # Visual properties have to be the same for all entities!
        AttributeObservable(self, 'color', 'color', discretization=128, visual=True)
        # AttributeObservable(self, 'radius', 'radius', discretization=10)
        # AttributeObservable(self, 'mass', 'mass', discretization=100)

    # def relativePosition(self, property=None):
    #     # - self.env.agents[0].shape.body.position
    #     relativePosition = self.body.position
    #     return [relativePosition.x, relativePosition.y]

    def absolutePosition(self, property=None):
        return [self.shape.body.position.x, self.shape.body.position.y]

    def positionToAgent(self, property=None):
        relativePosition = self.body.position - \
            self.world.child('Agent').shape.body.position
        return [relativePosition.x, relativePosition.y]

    # def move(self, parameters, property=None):
    #     # print("MOVE")
    #     # print(parameters)
    #     wl = min(max(parameters[0], -1), 1) ** 3
    #     wr = min(max(parameters[1], -1), 1) ** 3
    #     noise = 0.
    #
    #     self.body.apply_impulse_at_local_point(Vec2d(1.0, 0.0) * 1500 * float(wl + random.uniform(-noise, noise)) +
    #                                            Vec2d(0.0, 1.0) * 1500 * float(wr + random.uniform(-noise, noise)),
    #                                            (0, 0))

    def initPhysics(self, physics):
        inertia = pymunk.moment_for_circle(self.mass, 0, self.radius, (0, 0))
        body = pymunk.Body(self.mass, inertia)
        body.position = self.coords[0], self.coords[1]
        shape = pymunk.Circle(body, self.radius, (0, 0))
        shape.elasticity = 0.95
        physics.add(body, shape)
        self.shape = shape
        self.body = body

    def stopPhysics(self, physics):
        physics.remove(self.body, self.shape)

    def draw(self, base, drawOptions):
        if drawOptions.pygame:
            pygame.draw.circle(base, self.color, list(map(int, self.absolutePosition())), self.radius)
        if drawOptions.panda:
            if not self.pandaInit:
                self.pandaInit = True

                pt = PandaTools()
                pt.color = Vec4(*self.color, 1.)
                pt.cylinder(self.radius, 40.)
                node = pt.end()

                self.nodePath = base.render.attachNewNode(node)
                self.nodePath.setShaderAuto()
            self.nodePath.setPos(*self.body.position, 0.)
            
