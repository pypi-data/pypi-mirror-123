import numpy as np
from gym import spaces
from trucks_and_drones.obs import CustomObs

class NodeEncoderObs2(CustomObs):

    def __init__(self, temp_db):
        super(NodeEncoderObs2, self).__init__(temp_db)

        self.num_vec_inputs = 10
        self.num_node_inputs = 11
        self.num_connections = 10

    def obs_space(self):
        return spaces.Dict({
            'vector': spaces.Box(low=0, high=1, shape=(11,)),
            'nodes': spaces.Box(low=-1, high=1, shape=(11, 11,)),  # inputs
            'cur_node_idx': spaces.Discrete(11)
        })

    def observe_state(self):

        # Nodes:
        n_coord = self.temp_db('n_coord')
        n_inputs = []
        for i in range(len(n_coord)):
            distance = np.ravel(self.calc_euclidean_distance(n_coord[i], n_coord) / 10)
            n_inputs.append(distance)

        return {
            'vector': np.array(self.temp_db.status_dict['n_items']),
            'nodes': np.array(n_inputs),
            'cur_node_idx': np.array(self.get_node_index_by_coord(self.temp_db('v_coord', 0)))
        }
