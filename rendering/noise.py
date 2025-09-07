import numpy as np
from matplotlib import pyplot as plt
class Noise():
    def __init__(self, resolution, seed=None):
        self.resolution = resolution
        self.seed = seed

    def sample(self):
        pass

    def generate_texture(self):
        tex = np.zeros((self.resolution, self.resolution))
        for i in range(self.resolution):
            for j in range(self.resolution):
                uv = np.array([i/self.resolution, j/self.resolution])
                tex[j,i] = self.sample(uv)

        plt.imshow(tex, cmap='gray')
        plt.axis('off')
        plt.show()

        # Save it
        plt.imsave('noise.png', tex, cmap='gray')
        return tex

class ValueNoise(Noise):
    def __init__(self, div, resolution, seed=None):
        super().__init__(resolution, seed)
        self.div = div
        # arr = np.full((div,div), np.random.uniform(0,1,))
        self.grid = np.random.uniform(0,1,(div,div))

    def sample(self, uv):
        u = uv[0]
        v = uv[1]
        assert 0 <= u <= 1 and 0 <= v <= 1, f"UV coordinates out of range!"+\
            (f" U outside of bounds: {u}" if not 0 <= u <= 1 else f" V outside of bounds: {v}")

        epsilon = 1e-6  # avoid out-of-bounds
        u = min(u, 1 - epsilon)
        v = min(v, 1 - epsilon)

        x = u * (self.div - 1)
        y = v * (self.div - 1)

        x0 = int(np.floor(x))
        y0 = int(np.floor(y))
        x1 = min(x0 + 1, self.div - 1)
        y1 = min(y0 + 1, self.div - 1)

        dx = x - x0
        dy = y - y0

        bl = self.grid[y0, x0]
        br = self.grid[y0, x1]
        tl = self.grid[y1, x0]
        tr = self.grid[y1, x1]

        bottom = bl * (1 - dx) + br * dx
        top = tl * (1 - dx) + tr * dx
        value = bottom * (1 - dy) + top * dy
        return value

class PerlinNoise(Noise):
    def __init__(self, div, resolution, seed=None):
        super().__init__(resolution, seed)
        # self.seed = 
        self.div = div
        self.grid = np.random.uniform(0,1,(div,div,2))
        norms = np.linalg.norm(self.grid, axis=-1, keepdims=True)
        self.grid = self.grid / np.maximum(norms, 1e-8)

        # bilinearly interpolate each pixel

    def sample(self, uv):
        u = uv[0]
        v = uv[1]
        assert 0 <= u <= 1 and 0 <= v <= 1, f"UV coordinates out of range!"+\
            (f" U outside of bounds: {u}" if not 0 <= u <= 1 else f" V outside of bounds: {v}")

        epsilon = 1e-6  # avoid out-of-bounds
        uv[0] = min(uv[0], 1 - epsilon)
        uv[1] = min(uv[1], 1 - epsilon)
        # uv = min(uv, 1-epsilon)

        xy = uv * (self.div - 1)
        x = xy[0]
        y = xy[1]

        x0 = int(np.floor(x))
        y0 = int(np.floor(y))
        x1 = min(x0 + 1, self.div - 1)
        y1 = min(y0 + 1, self.div - 1)

        dx = x - x0
        dy = y - y0

        bl_pos = np.array([x0,y0])
        br_pos = np.array([x1,y0])
        tl_pos = np.array([x0,y1])
        tr_pos = np.array([x1,y1])

        bl_vec = self.grid[y0, x0]
        br_vec = self.grid[y0, x1]
        tl_vec = self.grid[y1, x0]
        tr_vec = self.grid[y1, x1]

        bl = np.dot(bl_vec, bl_pos - xy)
        br = np.dot(br_vec, br_pos - xy)
        tl = np.dot(tl_vec, tl_pos - xy)
        tr = np.dot(tr_vec, tr_pos - xy)

        bottom = bl * (1 - dx) + br * dx
        top = tl * (1 - dx) + tr * dx
        value = bottom * (1 - dy) + top * dy
        # value = self._smooth(value)
        return value
    
    def _smooth(self, x):
        return 6 * x **5  -15 * x ** 4 + 10 * x ** 3