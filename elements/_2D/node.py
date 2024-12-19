from element import Element2D
class NodeGraph(Element2D):
    def __init__(self, value, *connections):
        self.value = value
        self.connections = connections

    def draw(self):
        pass