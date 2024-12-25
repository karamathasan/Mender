class Presentation():
    def __init__(self, *scenes):
        self.scenes = list(*scenes)
        self.currentIndex = 0
    
    def add(self, scene):
        self.scenes.append(scene)

    def next(self):
        if self.currentIndex < len(self.scenes):
            self.currentIndex += 1 

    def run(self, dt: float):
        self.scenes[self.currentIndex].render()
