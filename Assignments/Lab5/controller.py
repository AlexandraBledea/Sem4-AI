import random

from domain.ant import Ant
from domain.graph import Graph
from domain.map import Map
from domain.constants import Constants


class Controller:

    def __init__(self):

        self._map = Map()

        self._map.randomMap()

        self._graph = Graph(self._map)

        self._sensor_distances = self._graph.sensor_distances
        self._pheromone_intensities = {}

        self.init_pheromone()

    @property
    def map(self):
        return self._map

    @property
    def graph(self):
        return self._graph

    def init_pheromone(self):

        for sensor1 in self._graph.sensors:
            self._pheromone_intensities[sensor1] = {}

            for sensor2 in self._graph.sensors:

                if sensor1._x == sensor2._x and sensor1._y == sensor2._y:
                    self._pheromone_intensities[sensor1][sensor2] = 0.0
                else:
                    # each road has as initial pheromone the value 1
                    self._pheromone_intensities[sensor1][sensor2] = 1.0

    def epoch_simulation(self, ant_count=Constants.ANT_COUNT, rho=Constants.RHO, q0=Constants.QO, alpha=Constants.ALPHA,
                         beta=Constants.BETA):

        sensors_charged = []

        ant_list = [Ant(self._graph.sensors[random.randint(0, Constants.SENSOR_COUNT - 1)]) for _ in range(ant_count)]

        for ant in ant_list:

            while ant.make_next_move(self.graph.sensor_distances, self._pheromone_intensities, alpha, beta, q0):
                pass

            # we evaluate the ant after all the moves it could have done, have been made
            ant.evaluate()

        # we simulate the pheromone evaporation for all the roads
        for sensor1 in self._pheromone_intensities:
            for sensor2 in self._pheromone_intensities:
                self._pheromone_intensities[sensor1][sensor2] *= (1 - rho)

        # we increase the pheromone intensity for each road the ants traversed
        for ant in ant_list:

            if ant.get_evaluation != 0:
                increase_intensity = 1.0 / float(Constants.BATTERY - ant.left_battery)
                sensors_charged = ant.sensor_order
            else:
                increase_intensity = 0

            for index in range(len(sensors_charged) - 1):

                sensor1 = sensors_charged[index]
                sensor2 = sensors_charged[index + 1]
                self._pheromone_intensities[sensor1][sensor2] += increase_intensity

        return self.select_best_ant(ant_list)

    def select_best_ant(self, ant_list):
        best_ant = None
        best_evaluation = 0

        # the best ant is the one with the best evaluation
        for ant in ant_list:
            if ant.get_evaluation > best_evaluation:
                best_evaluation = ant.get_evaluation
                best_ant = ant

        return best_ant

    def update_best_solution(self, best_sol):

        current_solution = self.epoch_simulation()

        if current_solution is None:
            return best_sol

        # if there is no better solution or an aunt with the same evaluation, but with more remaining battery, it means its better, so we update the best solution
        if best_sol is None or (current_solution.get_evaluation > best_sol.get_evaluation) or \
                (current_solution.get_evaluation == best_sol.get_evaluation and current_solution.left_battery > best_sol.left_battery):
            return current_solution

        return best_sol

    def run(self):

        bestSolution = None
        for _ in range(Constants.EPOCH_COUNT):
            bestSolution = self.update_best_solution(bestSolution)

        return bestSolution