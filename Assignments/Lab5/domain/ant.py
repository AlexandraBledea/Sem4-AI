from domain.constants import Constants
import random


class Ant:

    def __init__(self, start_sensor, battery=Constants.BATTERY):

        # Each ant at the beginning is placed on a random sensor
        # Each ant has a list with the sensors it visits, in the order it visits them
        self._sensor_order = [start_sensor]
        self._evaluation = 0  # this is basically the fitness, named differently

        # represents the last amount of energy we transferred to a sensor
        self._last_transfer = 0

        # we subtract from the start the maximum non-wasteful energy we can apply on the start sensor
        self._battery_left = battery - start_sensor.get_max_energy_level


    @property
    def sensor_order(self):
        return self._sensor_order

    @property
    def get_evaluation(self):
        return self._evaluation

    @property
    def left_battery(self):
        return self._battery_left

    def get_current_possible_moves(self, sensor_distances):

        moves = []

        # the last element of sensor_order list is the current one
        current_sensor = self._sensor_order[-1]

        # we take the distances computed for the current sensor to all the other sensors
        # where the key is the destination sensor and the value is the distance to it
        current_distances = sensor_distances[current_sensor]

        for sensor in current_distances:

            # 1) if the sensor is accessible from the current sensor
            # 2) if the sensor hasn't been visited yet
            # 3) if the distance to the sensor is within the battery limit
            if current_distances[sensor] != Constants.INF and (sensor not in self._sensor_order) and current_distances[sensor] <= self._battery_left:
                moves.append(sensor) # we add it in the sensor_order list

        # we return the list with the sensors which are possible to be visited
        return moves

     def make_next_move(self, sensor_distance, pheromone_intensities, alpha, beta, q0):

        possible_moves = self.get_current_possible_moves(sensor_distance)

        # We check whether there are possible moves or not
        # If there are no possible moves, we exit with false
        if len(possible_moves) == 0:
            return False

        sensor_with_max_coefficient = None

        probability_coefficients = {}

        max_coefficient = 0
        sum_coefficients = 0

        # We take the last sensor form the sensor_order
        current_sensor = self._sensor_order[-1]

        # We take the distances from the current sensor to all the other sensors
        # key - destination sensor, value - distance to it
        current_distances = sensor_distance[current_sensor]

        # We compute the probability coefficients for each of the next possible move, namely TAU^ALPHA * NU^BETA
        # So basically (kind of) we compute for each sensor, the probability for it to be choosen
        for sensor in possible_moves:

            attractivity = 1.0 / float(current_distances[sensor])  # TAU
            intensity = pheromone_intensities[current_sensor][sensor]  # NU

            probability_coefficients[sensor] = (intensity ** alpha) * (attractivity ** beta)

            if probability_coefficients[sensor] > max_coefficient:
                max_coefficient = probability_coefficients[sensor]
                sensor_with_max_coefficient = sensor

            sum_coefficients += probability_coefficients[sensor]

        q = random.random()

        selected_sensor = None

        # Here we have the probability q0 to pick the best sensor with the maximum coefficient (probability computed before)
        if q < q0:
            selected_sensor = sensor_with_max_coefficient
        else:

            # Here we do a stochastic proportional selection
            while selected_sensor == None:

                for sensor in probability_coefficients:

                    r = random.random()
                    p = probability_coefficients[sensor] / sum_coefficients

                    if r < p:
                        selected_sensor = sensor
                        break

        # We subtract from the battery the distance from the current sensor to the selected one
        self._battery_left -= sensor_distance[current_sensor][selected_sensor]

        # We add the selected sensor to the sensor_order
        self._sensor_order.append(selected_sensor)

        # Here we can have the case when we don't have sufficient left battery to transfer to the sensor the maximum energy it can receive
        # So in this case, we transfer to the sensor the left battery we have
        transferable_energy = min([self._battery_left, selected_sensor.get_max_energy_level])

        # We subtract from the battery the energy we can transfer to the sensor
        self._battery_left -= transferable_energy

        self._last_transfer = transferable_energy

        return True

    def evaluate(self):
        # Here the "fitness", basically represents the total number of accessible positions every ant can reach
        total_accessible_positions = 0

        for index in range(len(self._sensor_order) - 1):

            sensor = self._sensor_order[index]
            total_accessible_positions += sensor.get_accessible_positions[sensor.get_max_energy_level]

        # here the last sensor can represent a special case
        # it may or may not have been charged with its maximum non-wasteful energy
        # so here we take into account the last transfered energy

        total_accessible_positions += self._sensor_order[-1].get_accessible_positions[self._last_transfer]

        self._evaluation = total_accessible_positions

    def __str__(self):

        string = "Ant{ sensor_order["

        for sensor in self._sensor_order:
            string += str(sensor) + ", "

        string += "] ; " + "evaluation=" + str(self._evaluation) + " ; " + "last transfered=" + str(self._last_transfer) + "battery left=" + str(self._battery_left) + "}"