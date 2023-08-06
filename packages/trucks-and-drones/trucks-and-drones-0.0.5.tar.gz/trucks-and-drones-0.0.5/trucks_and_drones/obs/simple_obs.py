import numpy as np
from gym import spaces
from trucks_and_drones.obs import CustomObs

class SimpleObs(CustomObs):

    def __init__(self, temp_db, keys=None):
        super(SimpleObs, self).__init__(temp_db)

        if keys is None:
            keys = ['v_coord', 'v_dest', 'c_coord', 'd_coord', 'demand','v_items']
        self.keys = keys

        self.num_inputs = 64 #self.count_num_inputs(keys)

    def obs_space(self):
        return spaces.Box(low=0, high=1, shape=(self.num_inputs,))

    def observe_state(self):

        inputs = np.array([])
        for key in self.keys:
            if self.check_if_coord(key):
                inputs = np.append(inputs, self.coord_to_contin(key, True))
            else:
                inputs = np.append(inputs, self.value_to_contin(key))

        distances = np.array([])
        distances = np.append(distances, self.manhatten_distances_from_vehicle(0, consider_speed=False))
        distances = np.append(distances, self.euclidean_distances_from_vehicle(1, consider_speed=False))

        distances = self.min_max_scaler(distances, val_low=0, val_high=np.max(self.temp_db.grid))

        return np.append(inputs,distances)
