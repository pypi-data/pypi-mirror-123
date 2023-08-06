import numpy as np
from gym import spaces
from trucks_and_drones.acts import CustomAction


class TSPDroneAction(CustomAction):


    def __init__(self, temp_db, simulation):
        super(TSPDroneAction).__init__(temp_db, simulation)

    def reset(self):
        self.truck_action_waits = False
        self.drone_action_waits = False

    def action_space(self):
        return spaces.MultiDiscrete([self.temp_db.num_customers,self.temp_db.num_customers])

    def _truck_action(self):
        truck = self.temp_db.base_groups['vehicles'][0]  # vehicle with index 0

    def _drone_action(self):
        drone = self.temp_db.base_groups['vehicles'][1]  # vehicle with index 1

    def _truck_transporting_drone_action(self):
        truck = self.temp_db.base_groups['vehicles'][0]  # vehicle with index 0
        drone = self.temp_db.base_groups['vehicles'][1]  # vehicle with index 1

    def decode_actions(self, actions):
        truck = self.temp_db.base_groups['vehicles'][0]  # vehicle with index 0
        drone = self.temp_db.base_groups['vehicles'][1]  # vehicle with index 1

        #action_0 = int(input('Enter truck action: '))
        #action_1 = int(input('Enter drone action: '))

        #actions = np.array([action_0, action_1])

        #print(actions)

        reward = 0
        done_truck = False
        done_drone = False
        drone_is_transported = False

        # Truck:
        if not self.truck_action_waits:
            time_frame_truck, reward_truck, done_truck = self.to_customer(
                customer_idx=int(actions[0]),
                vehicle=truck,
                terminate_on_mistake=False,
                mistake_penalty=0,
                additional_reward=0,
            )
            reward += reward_truck
            self.temp_db.time_till_fin[0] = time_frame_truck
            #print('time_frame_truck',time_frame_truck)
            #print('reward_truck',reward_truck)
            #print('done_truck',done_truck)

        # Drone:
        if not self.drone_action_waits:
            time_frame_drone, reward_drone, done_drone = self.to_customer(
                customer_idx=int(actions[1]),
                vehicle=drone,
                terminate_on_mistake=False,
                mistake_penalty=0,
                additional_reward=0,
            )
            reward += reward_drone
            self.temp_db.time_till_fin[1] = time_frame_drone
            #print('time_frame_drone', time_frame_drone)
            #print('reward_drone', reward_drone)
            #print('done_drone', done_drone)

        # drone and truck are at the same node and have same destination
        if (self.temp_db.status_dict['v_dest'][0] == self.temp_db.status_dict['v_dest'][1]).all() and (
                self.temp_db.status_dict['v_coord'][0] == self.temp_db.status_dict['v_coord'][1]).all():
            drone_is_transported = True
            self.temp_db.time_till_fin[1] = np.copy(self.temp_db.time_till_fin[0])
            #print('drone is transported')

        # Terminate episode if mistakes were made
        if done_truck or done_drone or np.isnan(self.temp_db.time_till_fin[0]) or np.isnan(self.temp_db.time_till_fin[1]):
            return True, reward - 10 # additional terminal penalty

        if not drone_is_transported:
            cur_vehicle_idx = np.argmin(self.temp_db.time_till_fin)
        else:
            cur_vehicle_idx = 0

        time_frame = self.temp_db.time_till_fin[cur_vehicle_idx] # get current timeframe
        self.temp_db.time_till_fin[cur_vehicle_idx] = 0

        if cur_vehicle_idx == 0:
            vehicle = truck
            self.truck_action_waits = False

            if drone_is_transported:
                self.drone_action_waits = False
                self.temp_db.time_till_fin[1] = 0
            else:
                self.drone_action_waits = True
                self.temp_db.time_till_fin[1] = self.temp_db.time_till_fin[1] - time_frame

        else:
            vehicle = drone
            self.drone_action_waits = False
            self.truck_action_waits = True
            self.temp_db.time_till_fin[0] = self.temp_db.time_till_fin[1] - time_frame

        if self.temp_db.status_dict['v_items'][1] != 0 and self.temp_db.status_dict['n_items'][int(actions[cur_vehicle_idx]) + 1]:
            reward += 10

        vehicle.set_current_coord_to_dest()  # 'jump' to destination
        if cur_vehicle_idx == 0:
            self.simple_demand_satisfaction(customer_idx=int(actions[0]))  # set demand to zero

            if drone_is_transported:
                drone.set_current_coord_to_dest()  # 'jump' transported drone to destination

        else:
            if self.temp_db.status_dict['v_items'][1] != 0: # if drone has cargo
                self.simple_demand_satisfaction(customer_idx=int(actions[1]))
                self.temp_db.status_dict['v_items'][1] = 0 # drone has only one cargo slot


        if time_frame == 0:
            cur_vehicle_idx = np.argmax(self.temp_db.time_till_fin)
            time_frame = self.temp_db.time_till_fin[cur_vehicle_idx]  # get current timeframe
            self.temp_db.time_till_fin[cur_vehicle_idx] = 0

            if cur_vehicle_idx == 0:
                vehicle = truck
                self.truck_action_waits = False

                if drone_is_transported:
                    self.drone_action_waits = False
                    self.temp_db.time_till_fin[1] = 0
                else:
                    self.drone_action_waits = False
                    self.temp_db.time_till_fin[1] = self.temp_db.time_till_fin[1] - time_frame

            else:
                vehicle = drone
                self.drone_action_waits = False
                self.truck_action_waits = False
                self.temp_db.time_till_fin[0] = self.temp_db.time_till_fin[1] - time_frame

            if self.temp_db.status_dict['v_items'][1] != 0 and self.temp_db.status_dict['n_items'][int(actions[cur_vehicle_idx]) + 1]:
                reward += 10

            vehicle.set_current_coord_to_dest()  # 'jump' to destination
            if cur_vehicle_idx == 0:
                self.simple_demand_satisfaction(customer_idx=int(actions[0]))  # set demand to zero

                if drone_is_transported:
                    drone.set_current_coord_to_dest()  # 'jump' transported drone to destination

            else:
                if self.temp_db.status_dict['v_items'][1] != 0: # if drone has cargo
                    self.simple_demand_satisfaction(customer_idx=int(actions[1]))
                    self.temp_db.status_dict['v_items'][1] = 0 # drone has only one cargo slot


        reward -= time_frame
        self.temp_db.total_time += time_frame  # logging

        # truck and drone at the same location, drone gets full cargo
        if (self.temp_db.status_dict['v_coord'][0] == self.temp_db.status_dict['v_coord'][1]).all():
            self.temp_db.status_dict['v_items'][1] = 1
            drone.range_restr.reset() # reset range of drone

        # terminate if all demands are satisfied
        if self.check_demands():

            if (self.temp_db.status_dict['v_coord'][0] == self.temp_db.status_dict['v_coord'][1]).all():
                truck.set_node_as_destination(0)  # set destination to the single depot with index 0
                drone.set_node_as_destination(0)  # set destination to the single depot with index 0
                time_frame, error_signal = truck.calc_move_time(check_if_dest_reachable=True) # only truck needs to be checked

                if error_signal or np.isnan(time_frame):
                    return True, reward - 10

                truck.set_current_coord_to_dest() # move
                drone.set_current_coord_to_dest() # move

                return True, reward - time_frame + 10

            else:

                # Try to move drone to depot,
                # assuming this is always better:
                drone.set_node_as_destination(0)
                time_frame_drone, error_signal = drone.calc_move_time(check_if_dest_reachable=True)

                if not error_signal: # drone is able move to depot on its own
                    truck.set_node_as_destination(0)
                    time_frame_truck, error_signal = truck.calc_move_time(
                        check_if_dest_reachable=True)  # truck moves also to depot on its own

                    if error_signal or np.isnan(time_frame_drone) or np.isnan(time_frame_truck):
                        return True, reward - 10

                    time_frame = np.max([time_frame_truck, time_frame_drone])
                    truck.set_current_coord_to_dest()  # move
                    drone.set_current_coord_to_dest()  # move

                    return True, reward - time_frame + 10

                else: # drone has to be transported by truck:
                    self.temp_db.status_dict['v_dest'][0] = np.copy(self.temp_db.status_dict['v_coord'][1])
                    time_frame_truck_to_drone, error_signal = truck.calc_move_time(check_if_dest_reachable=True)

                    if error_signal or np.isnan(time_frame_truck_to_drone):
                        return True, reward - 10

                    truck.set_current_coord_to_dest()

                    truck.set_node_as_destination(0)  # set destination to the single depot with index 0
                    drone.set_node_as_destination(0)  # set destination to the single depot with index 0

                    time_frame, error_signal = truck.calc_move_time(
                        check_if_dest_reachable=True)  # only truck needs to be checked

                    if error_signal or np.isnan(time_frame):
                        return True, reward - 10

                    truck.set_current_coord_to_dest()  # move
                    drone.set_current_coord_to_dest()  # move
                    return True, reward - time_frame - time_frame_truck_to_drone  + 10

        return False, reward
