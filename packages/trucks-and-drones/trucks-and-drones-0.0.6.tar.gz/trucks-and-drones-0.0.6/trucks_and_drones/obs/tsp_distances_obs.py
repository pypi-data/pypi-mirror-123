import numpy as np
from gym import spaces
from trucks_and_drones.obs import CustomObs

class NodeDistancesObs(CustomObs):

    def __init__(
            self,
            num_inputs,
            include_depot=True,
            sort_nearest=False,
            zero_pad_no_demand=True,
            max_nodes_per_input=None, # only usable when sort_nearest is True
    ):
        super(NodeDistancesObs, self).__init__()

        self.num_inputs = num_inputs
        self.include_depot = include_depot
        self.sort_nearest = sort_nearest
        self.zero_pad_no_demand = zero_pad_no_demand

        if not max_nodes_per_input is None and not sort_nearest:
            Exception('If number of nodes per input are limited with max_nodes_per_input, the nodes have to be sorted. Set sort_nearest to True')

        self.max_nodes_per_input = max_nodes_per_input

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
