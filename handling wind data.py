import numpy as np

class Wind:
    
    def __init__(self):
        self.speed  = 0
        self.degree = 0
        self.vector = 0
        self.u = 0
        self.v = 0
        
    def to_vector(self, deg, speed):
        self.degree = deg
        self.speed  = speed
        u = np.sin(np.deg2rad(self.degree)) * self.speed * -1
        v = np.cos(np.deg2rad(self.degree)) * self.speed * -1
        
        self.vector = (u, v)
        return self.vector
    
    def to_speed(self, u, v):
        self.u = u
        self.v = v
        return np.sqrt(u**2 + v**2)
    
    def to_degree(self, u, v):
        self.u = u * -1
        self.v = v * -1
        deg = np.rad2deg(np.arctan2(u, v))
        deg = np.where(deg > 0, deg, deg + 360.)
        return deg
