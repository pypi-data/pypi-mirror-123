import numpy as np
from notegame.shumo.load_data import load_tag_info


class Anchor:
    def __init__(self, loc):
        self.loc = loc
        self.distance = None

    def init(self):
        self.distance = np.zeros([self.loc.shape[0], self.loc.shape[0]])
        for i in range(self.loc.shape[0]):
            for j in range(self.loc.shape[0]):
                self.distance[i][j] = round(np.linalg.norm(self.loc[i] - self.loc[j]), 5)

    @staticmethod
    def new_instance1():
        loc = np.array([[0, 0, 1300], [5000, 0, 1700],
                        [0, 5000, 1700], [5000, 5000, 1300]])
        anchor = Anchor(loc=loc)
        anchor.init()
        return anchor

    @staticmethod
    def new_instance2():
        loc = np.array([[0, 0, 1200], [5000, 0, 1600],
                        [0, 3000, 1600], [5000, 3000, 1200]])
        anchor = Anchor(loc=loc)
        anchor.init()
        return anchor


class TagInfo:
    def __init__(self, path, anchor=None):
        self.tag_df = None
        self.anchor = anchor or Anchor.new_instance1()
        self.init(path)

    def init(self, path):
        self.tag_df = load_tag_info(path)

    def cul_distance(self):
        a = np.array(self.tag_df[['x', 'y', 'z']].values)
        for i in range(4):
            b = a - self.anchor.loc[i]
            self.tag_df[f'd{i}'] = np.round(np.linalg.norm(b, axis=1))
