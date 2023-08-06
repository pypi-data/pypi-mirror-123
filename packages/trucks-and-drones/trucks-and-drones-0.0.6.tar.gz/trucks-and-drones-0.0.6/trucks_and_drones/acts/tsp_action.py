import numpy as np
from trucks_and_drones import acts
from gym import spaces


class TSPAction(acts.CustomAction):

    def __init__(
            self,
            terminate_on_mistake=False,
            additional_reward=0,
            mistake_penalty=-10,
            terminal_reward=10, # if not early episode termination due to mistake!
    ):
        '''
        :param terminate_on_mistake: Early breaking the episode, if action was invalid (visiting a customer twice).
        :param additional_reward: Additional reward for performing a valid action.
        :param mistake_penalty: Penalty when performing an invalid action.
        :param terminal_reward: If not stopped early due to a mistake, the terminal reward will be added.
        '''
        super(TSPAction, self).__init__()

        self.terminate_on_mistake = terminate_on_mistake
        self.additional_reward = additional_reward
        self.mistake_penalty = mistake_penalty
        self.terminal_reward = terminal_reward

    def action_space(self):
        '''
        The gym environment will call this method to get the action space.
        Hence, this method is always required. In this example, the action corresponds to
        choosing the index of a node to travel to (the action space is discrete).
        '''
        return spaces.Discrete(self.temp_db.num_customers)

    def decode_actions(self, actions):
        '''
        This method is also required, since this will be the main simulation about what happens,
        when an action is chosen.
        '''

        # Get the vehicle object from the database.
        # Because only one truck exists, the vehicle is indexed with zero.
        # This has to be a locale variable, since the vehicle object will not be the same,
        # when resetting the environment.
        vehicle = self.temp_db.base_groups['vehicles'][0]

        # Calculate the time to move and check if action is valid,
        # with the `to_customer` method from the base class.
        # This method can also check if the chosen action is valid (customer was not visited yet)
        # If the action was invalid, the episode can be terminated,
        # when you chose to set terminate_on_mistake as True (done will be set to True).
        # Additionally a mistake penalty can be applied (Note that this number has to be negative),
        # or a reward, when the action was valid (this might be useful, if you want positive rewards)
        # If neither `mistake_penalty` or `additional_reward` is used,
        # the returned `reward ` will be zero.
        time_frame, reward, done = self.to_customer(
            customer_idx=int(actions),
            vehicle=vehicle,
            terminate_on_mistake=self.terminate_on_mistake,
            additional_reward=self.additional_reward,
            mistake_penalty=self.mistake_penalty
        )

        # Depending on the vehicles restrictions, the calculated time_frame,
        # which is the vehicles travel time to the chosen node, can be np.nan.
        # In this case the reward can't include the traval time as a penalty,
        # because nan can't be interpret by the agent.
        # For the standard restrictions of a truck, this will never be the case,
        # but I included the if statement here for the sake of avoiding future errors.
        if not np.isnan(time_frame):
            reward -= time_frame
            self.temp_db.total_time += time_frame  # logging, always do this for proper results!

        # If the episode is not terminated, because of an invalid action,
        # the vehicles destination can be set as the new current position,
        # with the vehicle method `set_current_coord_to_dest`.
        # This corresponds to "jumping" to the destination and is only valid,
        # because the vanilla tsp consists of only one vehicle.
        # Additionally, the method `simple_demand_satisfaction` from the base class is used,
        # to set the demand of the chosen customer to zero
        # (initially each customer has a demand of one).
        if not done:
            vehicle.set_current_coord_to_dest()  # 'jump' to destination
            self.simple_demand_satisfaction(customer_idx=int(actions))  # set demand to zero

        # The last part of this method, corresponds to the assumption,
        # that the vehicle has to return to the depot, after all customers are visited.
        # For this purpose the method `check_demands` from the base class is called,
        # to check whether all demands are satisfied. If this is the case and the episode
        # wasn't already terminated, the depot will be selected as destination.
        # After setting the destination, the vehicle method `calc_move_time` is used,
        # to calculate the travel time and check if any vehicle restriction was violated.
        if self.check_demands() and not done:
            vehicle.set_node_as_destination(0)  # set destination to the single depot with index 0
            time_frame, error_signal = vehicle.calc_move_time(check_if_dest_reachable=True)

            # Like in the code above, the reward should only updated,
            # if the time_frame is not np.nan.
            if not np.isnan(time_frame):
                reward -= time_frame
                self.temp_db.total_time += time_frame  # logging

            # The error_signal will be true, if any vehicle restriction was violated.
            # Again, this is only included to avoid future errors,
            # even though with the standard truck parameters this will never be true.
            # Like in the example above, the vehicle will "jump" to its chosen destination,
            # with the vehicle method `set_current_coord_to_dest`.
            # Additionally a terminal reward is added, which can either be used to mirror the rewards
            # of the method `to_customer` or as a much larger terminal reward that corresponds
            # to completing the whole episode successfully (in this case, you probably don't want
            # to use additional rewards when calling `to_customer`).
            if not error_signal:
                vehicle.set_current_coord_to_dest()  # 'jump' to destination
                reward += self.terminal_reward  # terminal reward
            done = True  # episode is finished

        return done, reward  # always has to be returned by this method