import numpy as np
from gym import spaces
from trucks_and_drones.obs import CustomObs

class CoordObs(CustomObs):

    def __init__(
            self,
            num_inputs,
            keys=None,
            zero_pad_no_demand=True,
    ):
        '''
        :param num_inputs: Number of inputs
        :param keys: Keys are used to get the values from the database. In this case only keys corresponding to coordinates are valid.
        :param zero_pad_no_demand: Sets customer coordinates to zero, when their demand is already satisfied.
        '''
        super(CoordObs, self).__init__()

        self.num_inputs = num_inputs

        if keys is None:
            keys = ['v_coord', 'c_coord', 'd_coord']
        self.keys = keys

        self.zero_pad_no_demand = zero_pad_no_demand

    def obs_space(self):
        '''
        Necessary method, called by the gym environment to return the observation space.
        '''
        return spaces.Box(low=0, high=1, shape=(self.num_inputs,))

    def observe_state(self):
        '''
        Necessary method, called by the gym environment to return the current observation.
        '''
        # Creating empty array
        inputs = np.array([])

        # Iterating through each key, to get the data
        for key in self.keys:
            # Using the method `coord_to_contin` from the base class,
            # to transform the coordinates to normalized values.
            # Additionally, this method will zero-pad customers coordinates,
            # when set_coord_with_no_demand_to_zero is set to true.
            # Returns of the method are appended to the numpy array `inputs`.
            inputs = np.append(inputs, self.coord_to_contin(key, set_coord_with_no_demand_to_zero=self.zero_pad_no_demand))

        # returning observations as a numpy array (always has to be returned by this method)
        return inputs


class FromKeysObs(CustomObs):

    def __init__(
            self,
            num_inputs,
            keys=None,
            zero_pad_no_demand=False
    ):
        super(FromKeysObs, self).__init__()

        self.num_inputs = num_inputs

        if keys is None:
            keys = ['v_coord', 'c_coord', 'd_coord', 'demand']
        self.keys = keys

        self.zero_pad_no_demand = zero_pad_no_demand

    def obs_space(self):
        return spaces.Box(low=0, high=1, shape=(self.num_inputs,))

    def observe_state(self):

        inputs = np.array([])
        for key in self.keys:
            if self.check_if_coord(key):
                inputs = np.append(inputs, self.coord_to_contin(key, self.zero_pad_no_demand))
            else:
                inputs = np.append(inputs, self.value_to_contin(key))

        return inputs
