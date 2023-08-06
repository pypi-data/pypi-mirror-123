import numpy as np
from gym import spaces
from trucks_and_drones.acts import CustomAction


class TSPAction(CustomAction):

    def __init__(self, temp_db, simulation):
        super(TSPAction).__init__(temp_db, simulation)

    def action_space(self):
        return spaces.Discrete(self.temp_db.num_customers)

    def decode_actions(self, actions):

        vehicle = self.temp_db.base_groups['vehicles'][0] # only one vehicle with index 0

        # calc the time to move and check if action is valid
        time_frame, reward, done = self.to_customer(
            customer_idx=int(actions),
            vehicle=vehicle,
            terminate_on_mistake=False
        )

        # if vehicle can move, update reward and log to total time (costs):
        # (under standard parameter/assumptions, this will always be the case)
        if not np.isnan(time_frame):
            reward -= time_frame
            self.temp_db.total_time += time_frame  # logging

        # if action was vaild, move and update demand:
        if not done:
            vehicle.set_current_coord_to_dest()  # 'jump' to destination
            self.simple_demand_satisfaction(customer_idx=int(actions))  # set demand to zero

        # check if all demands are satisfied,
        # if so return to depot
        if self.check_demands() and not done:
            vehicle.set_node_as_destination(0) # set destination to the single depot with index 0
            time_frame, error_signal = vehicle.calc_move_time(check_if_dest_reachable=True)

            if not np.isnan(time_frame):
                reward -= time_frame
                self.temp_db.total_time += time_frame  # logging

            if not error_signal:
                vehicle.set_current_coord_to_dest()  # 'jump' to destination
                reward += 10 # adding the additional reward, so the reward always stays positive for correct actions
            done = True

        return done, reward
