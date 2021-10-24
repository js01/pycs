import json
import random
import math
import traceback
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("cs." + __name__)

from PIL import ImageTk
from pycs.interfaces.WorldModelABC import WorldModelABC
from pycs.interfaces.DataLoaderABC import DataLoaderABC

class WorldObject:
    """
    An entity; used to define data associated with any object in the world model.

    Attributes:
        name:
        png:
        v:
        w:
        h:
    """

    def __init__(self, name, png, x, y, w, h):
        self.name = name
        self.png = png
        self.v = [x, y]
        self.w = w
        self.h = h        
        self.initialized = True

    @property
    def x(self):
        return self.v[0]
    
    @x.setter
    def x(self, u):
        self.v[0] = u

    @property
    def y(self):
        return self.v[1]
        
    @y.setter
    def y(self, u):
        self.v[1] = u

class LocalWorldModel(WorldModelABC):
    """
    A model of the world in local memory, stored in json.

    Attributes:
        world_objects:
    """

    def __init__(self, data_loader):

        self.world_objects = []
        with data_loader as dl:
            for obj in dl:
                logger.debug("creating object %s with data x=%d y=%d w=%d h=%d" % (obj.name, *obj.v, obj.w, obj.h))
                wo = WorldObject(obj.name, obj.filename, *obj.v, obj.w, obj.h)
                self.world_objects.append(wo)

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        if tb:
            print("".join(traceback.format_tb(tb)), type, value)
        return self

    def __iter__(self):
        for ent in self.world_objects:
            yield ent

    def __getitem__(self, x):
        pass
   
    def __setitem__(self, x, v):
        pass

    def _index(self):
        # fast spatial index for retrieving objects
        pass
    
    def update_object_x(self, i, new_x):
        self.world_objects[i].x = new_x
    
    def update_object_y(self, i, new_y):
        self.world_objects[i].y = new_y
        
    def query(self, v_ul, v_br):
        # query for objects in box between v_ul and v_br
        pass

    def find_near(self, x, y, r=300):
        logging.debug("querying near %d %d %d" % (x, y, r))
        res = []
        for wi, wo in enumerate(self.world_objects):
            # taxicab
            dr = math.fabs(wo.x - x) + math.fabs(wo.y - y)
            if dr < r:
                res.append((wi, dr))
        return [t[0] for t in sorted(res, key=lambda x:x[1])]

    def find_nearest(self, x, y):
        logging.debug("querying nearest %d %d" % (x, y))
        res = []
        for wi, wo in enumerate(self.world_objects):
            # taxicab
            dr = math.fabs(wo.x + ( wo.w / 2 ) - x) + math.fabs(wo.y + ( wo.h / 2) - y)
            res.append((wi, wo.x, wo.y, dr))
        mini = min(res, key=lambda x:x[3])
        logging.debug("found %d nearest!" % mini[0])
        return mini[0]


