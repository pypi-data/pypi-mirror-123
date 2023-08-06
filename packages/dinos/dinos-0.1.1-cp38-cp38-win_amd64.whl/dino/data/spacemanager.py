'''
    File name: dataset.py
    Author: Alexandre Manoury
    Python Version: 3.6
'''

import numpy as np
import math
import random
from scipy.spatial import cKDTree
from scipy.spatial.distance import euclidean

from exlab.modular.module import Module
from exlab.interface.serializer import Serializable
from exlab.utils.io import parameter

from .data import *
from .space import Space, SpaceKind
from .event import InteractionEvent
from .multispace import MultiColSpace, MultiColDataSpace, MultiRowDataSpace
from dino.representation.entity_manager import EntityManager, Entity


# import graphviz


class SpaceManager(Module, Serializable, EntityManager):
    def __init__(self, name, storesData=False, options={}, parent=None, entityCls=Entity):
        Module.__init__(self, parent=parent)
        Serializable.__init__(self)
        EntityManager.__init__(self, name, entityCls=entityCls)
        self.name = name
        self.spaces = []
        self.storesData = storesData
        self.options = options

        self.multiColSpaces = []
        self.multiRowSpaces = []

        self.events = {}

        self.computeSpaces()
    
    def _sid(self, serializer):
        return serializer.uid('spaceManager', self.name)

    def _serialize(self, serializer):
        dict_ = {}
        dict_.update(serializer.serialize(self, ['spaces', 'storesData']))
        return dict_

    @classmethod
    def _deserialize(cls, dict_, serializer, obj=None):
        if obj is None:
            obj = cls(dict_.get('storesData'),
                      options=dict_.get('options', {}))
        return super()._deserialize(dict_, serializer, obj)

    def _postDeserialize(self, dict_, serializer):
        serializer.set('spaceManager', self)
        serializer.deserialize(dict_.get('spaces', []))
        super()._postDeserialize(dict_, serializer)

    def __repr__(self):
        return f'SpaceManager({len(self.spaces)} spaces) and {EntityManager.__repr__(self)}'
    
    @property
    def size(self):
        return len(self.spaces)
    
    # Triggered when new data are added
    def updated(self):
        pass

    # Spaces
    def registerSpace(self, space):
        if space not in self.spaces:
            self.spaces.append(space)
            self.computeSpaces()

    def computeSpaces(self):
        self.actionSpaces = self.getActionSpaces(self.spaces)
        self.actionExplorationSpaces = self.getActionExplorationSpaces(self.spaces)
        self.actionPrimitiveSpaces = self.getActionPrimitiveSpaces(self.spaces)
        self.outcomeSpaces = self.getOutcomeSpaces(self.spaces)
    
    # Space conversion
    def convertSpace(self, space, kind=None, toData=None):
        toData = parameter(toData, self.storesData)  # space.canStoreData()
        kind = parameter(kind, space.kind)

        relatedSpace = next((s for s in self.spaces if s.kind.value == kind.value and s.linkedTo(space)), None)
        if relatedSpace is not None:
            return relatedSpace

        if toData:
            return space.createDataSpace(self, kind)
        else:
            return space.createLinkedSpace(self, kind)

    def convertSpaces(self, spaces, kind=None, toData=None):
        return [self.convertSpace(space, kind=kind, toData=toData) for space in spaces]

    def convertData(self, data, kind=None, toData=None):
        return data.convertTo(self, kind=kind, toData=toData)

    # Multi Spaces
    def _multiSpace(self, spaces, list_, type_, orderWise=False):
        # Only 1 space -> return the space itself
        if len(spaces) == 1:
            return spaces[0]

        # Look for exisiting multi space
        if orderWise:
            r = [s for s in list_ if s.spaces == spaces]
        else:
            r = [s for s in list_ if set(s.spaces) == set(spaces)]
        if len(r) == 0:
            s = type_(self, spaces)
            list_.append(s)
            return s
        else:
            return r[0]

    def _multiSpaceWeighted(self, spaces, list_, type_, weight=None, orderWise=False, weightSpaces=None):
        space = self._multiSpace(spaces, list_, type_, orderWise=orderWise)

        if weight:
            space.clearSpaceWeight()
            for subspace in weightSpaces:
                space.spaceWeight(weight, subspace)

        return space

    def multiColSpace(self, spaces, canStoreData=None, weight=None):
        # Flatten the list of spaces
        flatSpaces = list(set([subSpace for space in spaces for subSpace in space.cols if space is not None]))

        if len(flatSpaces) == 1:
            return flatSpaces[0]

        if canStoreData is None:
            if flatSpaces:
                dataSpaces = list(set([space.canStoreData()
                                       for space in flatSpaces]))
                if len(dataSpaces) > 1:
                    raise Exception(
                        f"All spaces should be a DataSpace or none: {flatSpaces}")
                canStoreData = dataSpaces[0]
            else:
                canStoreData = self.storesData

        return self._multiSpaceWeighted(flatSpaces, list_=self.multiColSpaces,
                                        type_=MultiColDataSpace if canStoreData else MultiColSpace, weight=weight, weightSpaces=spaces)

    def multiRowSpace(self, spaces, canStoreData=None):
        # spaces = list(set([subSpace for space in spaces for subSpace in space]))
        # spaces = list(set([space for space in spaces if space is not None]))
        spaces = [space for space in spaces if space is not None]

        if not spaces:
            return
        if len(spaces) == 1:
            return spaces[0]

        return self._multiSpaceWeighted(spaces, list_=self.multiRowSpaces, type_=MultiRowDataSpace, orderWise=True)

    # List Spaces
    def space(self, index_name, kind=SpaceKind.BASIC):
        return next(s for s in self.spaces if (s.name == index_name and (s.kind.value == kind.value or s.native == s))
                    or s.id == index_name)

    def spaceSearch(self, property=None, kind=SpaceKind.BASIC):
        if property:
            return next((s for s in self.spaces if s.boundProperty == property and s.kind.value == kind.value), None)
        return None

    def getActionSpaces(self, spaces):
        return [s for s in spaces if s.controllable() and s.kind == SpaceKind.BASIC]

    def getActionExplorationSpaces(self, spaces):
        return [s for s in spaces if s.controllable() and s.kind == SpaceKind.BASIC
                and not s.noaction]

    def getActionPrimitiveSpaces(self, spaces):
        return [s for s in spaces if s.primitive() and s.kind.value == SpaceKind.BASIC.value and not s.noaction]

    def getOutcomeSpaces(self, spaces):
        return [s for s in spaces if s.observable()
                and s.kind.value == SpaceKind.BASIC.value]

    # Data
    def addEvent(self, event, cost=1.):
        """Add data to the dataset"""
        event = event.clone()
        event.addToSpaces(cost=cost)
        self.logger.debug(f'Adding point {event} to dataset {self}', tag='dataset')
        self.events[event.iteration] = event

    def actions(self):
        return [event.actions for event in self.events]

    # def eventFromId(self, iteration):
    #     register = self.events[iteration]
    #     event = InteractionEvent(iteration)
    #     event.actions = ActionList(Action(
    #         *(SingleAction(t, self.getData(t, v).tolist()) for t, v in register.actions)))
    #     event.outcomes = Observation(
    #         *(SingleObservation(t, self.getData(t, v).tolist()) for t, v in register.outcomes))
    #     return event

    def getData(self, space_id, data_id):
        return self.space(space_id).data[data_id]
