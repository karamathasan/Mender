class Presentation():
    def __init__(self, *scenes):
        self.scenes = scenes
        self.currentIndex = 0

    def next(self):
        if self.currentIndex < len(self.scenes):
            self.currentIndex += 1 

    def run(self, dt: float):
        pass