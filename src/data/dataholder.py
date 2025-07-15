from abc import abstractmethod

class DataHolder():
    def __init__(self):
        self.data = None

    @abstractmethod
    def loadData(self):
        pass