from abc import ABC, abstractmethod, abstractproperty

class WorldObjectABC(ABC):
    @abstractproperty
    def data_dict(self): pass

class WorldModelABC(ABC):
    @abstractmethod
    def __iter__(self): pass
    @abstractmethod
    def __getitem__(self): pass
    @abstractmethod
    def __setitem__(self): pass
#    @abstractmethod
#    def __enter__(self): pass
#    @abstractmethod
#    def __exit__(self): pass
    @abstractmethod
    def update_object_x(self): pass
    @abstractmethod
    def update_object_y(self): pass    

