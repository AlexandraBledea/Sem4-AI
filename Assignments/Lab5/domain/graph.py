from domain.constants import Constants
from domain.sensor import Sensor
class Graph:

    def __init__(self, map):

        self._sensors = [] # basically the list of nodes
        self._map = map

        self.place_random_sensors()

        self.compute_sensor_parameters()

        '''
            keys - start sensors
            values - dictionaries having as key the finish sensors and values the distances to themselves
        '''

        self._sensor_distances = {}

        self.compute_distances_between_sensors()

    @property
    def sensors(self):
        return self._sensors

    @property
    def sensor_distances(self):
        return self._sensor_distances

    def compute_distances_between_sensors(self):

        for s1 in self._sensors:

            # we create spot in the dictionary for the sensor s1
            self._sensor_distances[s1] = {}

            for s2 in self._sensors:

                if s1._x == s2._x and s1._y == s2._y:

                    # from a sensor to itself the distance is always 0
                    self._sensor_distances[s1][s2] = 0

                else:
                    # we add in the dictionary the distance from sensor s1 to s2, as being computed by the BFS
                    self._sensor_distances[s1][s2] = self.BFS(s1._x, s1._y, s2._x, s2._y)

    def place_random_sensors(self, count = Constants.SENSOR_COUNT):
        # On the map, we mark the sensors (nodes) with 3

        # First we clear the current list of sensors
        self.sensors.clear()

        for _ in range(count):
            # We take a random empty square
            (x, y) = self._map.getEmptySquares()
            # We mark the sensor, and append it to the node list
            self._map.surface[x][y] = 3
            self._sensors.append(Sensor(x, y))

    def compute_sensor_parameters(self):
        # For each sensor from the list, we compute the maximum non-wasteful energy and the number of accessible points
        for sensor in self._sensors:
            sensor.compute_max_necessary_energy(self._map.surface)

    @staticmethod
    def validateCoords(x, y, surface):
        return 0 <= x < Constants.MAP_SIZE and 0 <= y < Constants.MAP_SIZE and (surface[x][y] == 0 or surface[x][y] == 3)

    def BFS(self, start_x, start_y, final_x, final_y):

        # We take a copy of the surface, because we will mark the visited squares directly on this map
        auxiliary_surface = self._map.surface.copy()

        # We create the distance dictionary, and mark the distance from the square to itself as being 0
        distance = {(start_x, start_y): 0}

        # We create the initial queue
        queue = [(start_x, start_y)]

        while len(queue) != 0:
            coords = queue.pop(0)

            for direction in Constants.DIRECTIONS:

                new_x = coords[0] + direction[0]
                new_y = coords[1] + direction[1]

                # If the new coordinates are valid we mark that square as being visited, update its distance and append it to the queue
                if Graph.validateCoords(new_x, new_y, auxiliary_surface):

                    auxiliary_surface[new_x][new_y] = 2

                    distance[(new_x, new_y)] = distance[(coords[0], coords[1])] + 1
                    queue.append((new_x, new_y))

                    # If we reach the final coordinates, we return the distance
                    if(new_x == final_x and new_y == final_y):
                        return distance[(final_x, final_y)]

        # Otherwise we return infinity, meaning that the coordinates are not reachable
        return Constants.INF

