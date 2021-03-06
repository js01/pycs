import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from pycs.interfaces.CommandABC import CommandABC

class ComLowerSelected(CommandABC):

    def __init__(self, image_collection):
        self.image_collection = image_collection
        self.focused_image = self.image_collection.get_selected()

    def execute(self):
        self.image_collection.select_image(self.focused_image)
        self.image_collection.lower_focused_image()

    def undo(self):
        self.image_collection.select_image(self.focused_image)
        self.image_collection.lift_focused_image()

class ComLiftSelected(CommandABC):

    def __init__(self, image_collection):
        self.image_collection = image_collection
        self.focused_image = self.image_collection.get_selected()

    def execute(self):
        self.image_collection.select_image(self.focused_image)
        self.image_collection.lift_focused_image()

    def undo(self):
        self.image_collection.select_image(self.focused_image)
        self.image_collection.lower_focused_image()
       

class ComDuplicate(CommandABC):

    def __init__(self, image_collection, wm, index, x, y):
        self.image_collection = image_collection
        self.world_model = wm
        self.x = x
        self.y = y
        self.index = index
        self.added = None

    def execute(self):
        x, y, i = self.x, self.y, self.index
        wo = self.world_model.duplicate_world_object(i, x, y)
        tmp_image = self.image_collection.add_image(wo.png, x, y, w=wo.w, h=wo.h, anchor="nw")
        self.added = tmp_added

    def undo(self):
        # TODO: delete
        pass


class ComFinishMove(CommandABC):
    
    def __init__(self, image_collection, world_model, newx, newy, selected_image):
        self.startx = world_model[selected_image].x
        self.starty = world_model[selected_image].y
        logger.debug("Creating a move command, starting at %s %s" % (self.startx, self.starty))

        self.newx = newx
        self.newy = newy
        self.selected = selected_image
        self.image_collection = image_collection
        self.world_model = world_model

    def __str__(self):
        return "ComFinishMove object " + str(hex(id(self))) + ", started at %s %s" % (self.startx, self.starty)
        
    def execute(self):
        self.image_collection.move_selected_image(self.newx, self.newy)
        selected_image = self.image_collection.get_selected()
        self.world_model.update_object_x(selected_image, self.newx)
        self.world_model.update_object_y(selected_image, self.newy)

    def undo(self):
        logger.debug("Started at %s %s, reverting there." % (self.startx, self.starty))
        self.image_collection.select_image(self.selected)
        self.image_collection.snap_move_selected_image(self.startx, self.starty)
        selected_image = self.image_collection.get_selected()
        self.world_model.update_object_x(selected_image, self.startx)
        self.world_model.update_object_y(selected_image, self.starty)

