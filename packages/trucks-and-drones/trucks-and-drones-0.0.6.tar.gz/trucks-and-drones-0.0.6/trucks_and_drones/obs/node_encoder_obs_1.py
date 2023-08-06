import numpy as np
from gym import spaces
from trucks_and_drones.obs import CustomObs

class NodeEncoderObs(CustomObs):

    def __init__(self, temp_db):
        super(NodeEncoderObs, self).__init__(temp_db)

        self.num_vec_inputs = 10
        self.num_node_inputs = 11
        self.num_connections = 10

    def obs_space(self):
        return spaces.Dict({
            'vector': spaces.Box(low=0, high=1, shape=(self.num_vec_inputs,)),
            'nodes_1': spaces.Box(low=-1, high=1, shape=(self.num_node_inputs, self.num_connections,)),  # inputs
            'nodes_2': spaces.Box(low=0, high=np.inf, shape=(1,)),  # cur index
            'nodes_3': spaces.Box(low=0, high=np.inf, shape=(self.num_node_inputs,self.num_connections,))  # indices of nearest nodes
        })

    def observe_state(self):

        # Nodes:
        n_coord = self.temp_db('n_coord')
        #n_vals = np.append(np.array([-1]), self.temp_db('demand'))
        n_inputs = []
        n_index_list = []
        for i in range(len(n_coord)):
            distance = np.ravel(self.calc_euclidean_distance(n_coord[i], n_coord) / 10)
            sorted = np.sort(distance)[1:11]
            sorted_indices = np.argsort(distance)[1:11]
            n_inputs.append(sorted)
            n_index_list.append(sorted_indices)

        cur_node_idx = self.get_node_index_by_coord(self.temp_db('v_coord', 0))
        #print(cur_node_idx)

        demands = []
        for idx in n_index_list[cur_node_idx]:
            demands.append(self.temp_db.status_dict['n_items'][idx])

        # Vector:
        vec_inputs = np.array(demands)
        #vec_inputs = np.append(self.temp_db('v_coord'))
        #vec_inputs = np.append(self.temp_db('v_dest'))

        return {
            'vector': vec_inputs,
            'nodes_1': np.array(n_inputs),
            'nodes_2': cur_node_idx,
            'nodes_3': np.array(n_index_list)
        }
