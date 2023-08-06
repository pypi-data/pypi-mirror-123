import numpy as np

class CustomAction:
    '''
    Base class for custom actions.
    '''

    def __init__(self,  temp_db, simulation):
        self.temp_db = temp_db
        self.simulation = simulation

    def build(self, temp_db, simulation):
        self.temp_db = temp_db
        self.simulation = simulation

    def action_space(self):
        pass

    def decode_actions(self, actions):
        pass

    def reset(self):
        pass

    def to_customer(
            self,
            customer_idx,
            vehicle,
            terminate_on_mistake=True,
            mistake_penalty=-10,
            additional_reward=10
    ):

        done = False
        reward = 0
        node_idx = customer_idx + self.temp_db.num_depots # transform customer index to node index

        # No demand, bad action:
        if self.temp_db.get_val('n_items')[node_idx] == 0:
            reward += mistake_penalty
            if terminate_on_mistake:
                done = True

        # Customer has demand:
        else:
            if not self.temp_db.status_dict['v_items'][vehicle.v_index] == 0:
                reward += additional_reward

        vehicle.set_node_as_destination(node_idx)

        # calculate move time and check if vehicle can actually move/ reach destination:
        time_frame, error_signal = vehicle.calc_move_time(check_if_dest_reachable=True)

        if error_signal:
            reward += mistake_penalty

        if terminate_on_mistake and error_signal:
            done = True

        return time_frame, reward, done

    def simple_demand_satisfaction(self, customer_idx):
        '''
        Assumes customers demand can be satisfied instantly without any restrictions,
        additional assumes infinite cargo of vehicle
        '''
        node_idx = customer_idx + self.temp_db.num_depots # transform customer index to node index
        self.temp_db.status_dict['n_items'][node_idx] = 0

    def check_demands(self):
        return bool(np.sum(self.temp_db.get_val('n_items')[self.temp_db.num_depots:]) == 0)

