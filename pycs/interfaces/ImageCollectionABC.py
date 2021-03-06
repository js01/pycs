from abc import ABC, abstractmethod

class ImageCollectionABC(ABC):

    @abstractmethod
    def pan(self):
        pass

    @abstractmethod
    def zoom(self):
        pass

    @abstractmethod
    def move_image(self, j):
        """ Move an image. """
        pass

