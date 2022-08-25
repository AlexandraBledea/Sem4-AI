from domain.constants import Constants
from domain.node import Node

class Sensor(Node):

    def __init__(self, x_coord, y_coord):
        super().__init__(x_coord, y_coord)
        self.__accessible_positions = [0 for _ in range(6)] # for each energy 0 -> 5
        self._max_energy = 0

        self.__accessible_positions[0] = 0

    def is_valid_coordinate(self, x, y, mapSurface):
        return 0 <= x < Constants.MAP_SIZE and 0 <= y < Constants.MAP_SIZE and mapSurface[x][y] != 1

    def compute_max_necessary_energy(self, map):
        # Like that, we keep into the array if more applied energy would discover any new area in a certain direction or not
        # 0 - UP, 1 - LEFT, 2 - DOWN, 3 - RIGHT

        blocked_direction = [False for _ in range(4)]

        current_accessible_positions = 0

        # We can apply minimum 0 energy and maximum 5 energy
        for energy in range(1, 6):
            for index in range(4):

                # If the direction is blocked (meaning we hit a block or the wall, there is no point in checking that direction again)
                if blocked_direction[index] == False:

                    dir = Constants.DIRECTIONS[index]
                    new_x = self._x + dir[0] * energy
                    new_y = self._y + dir[1] * energy

                    if not self.is_valid_coordinate(new_x, new_y, map):
                        blocked_direction[index] = True
                    else:
                        current_accessible_positions += 1
                        self.__accessible_positions[energy] = int(current_accessible_positions)

            # If the direction is blocked in all 4 directions, we exit with the previous number of energy
            index = 0
            while index < 4 and blocked_direction[index] == True:
                index += 1

            if index == 4:

                self._max_energy = energy - 1
                return

        self._max_energy = 5

    @property
    def get_max_energy_level(self):
        return self._max_energy

    @property
    def get_accessible_positions(self):
        return self.__accessible_positions

    def __str__(self):
        return "Sensor(x=" + str(self._x) + ", y=" + str(self._y) + ", max=" + str(self._max_energy) + ", " + str(self.__accessible_positions) + ")"













    # def compute_accessible_positions(self, mapSurface):
    #     # This function should be called after all the sensors have been placed
    #     directions = Constants.DIRECTIONS
    #     blocked_direction = [False for _ in range(len(directions))]
    #     # Here we compute the accessible positions from the sensor for each energy from 0 to 5
    #     # And we keep these values in the accessible_positions
    #     for energy in range(1, Constants.ENERGY_LEVELS):
    #         self.__accessible_positions[energy] = self.__accessible_positions[energy - 1]
    #         # We go through the directions
    #         for i in range(len(directions)):
    #             if not blocked_direction[i]:
    #                 # We check if the sensor is able to see that further, if so, we increase the accessible positions with 1
    #                 # Otherwise we mark that direction as being blocked and we move on
    #                 direction = directions[i]
    #                 if self.is_valid_coordinate(self._xCoord + direction[0] * energy, self._yCoord + direction[1] * energy, mapSurface):
    #                     self.__accessible_positions[energy] += 1
    #                 else:
    #                     blocked_direction[i] = True
    #
    #
    # def compute_max_energy_level(self):
    #     # We compute this such that no energy is wasted
    #     # This should be called after compute_accessible_positions
    #     for energy in range(Constants.ENERGY_LEVELS - 1):
    #         if self.__accessible_positions[energy] == self.__accessible_positions[energy + 1]:
    #             self._maximum_energy_level = energy
    #             return
    #     self._maximum_energy_level = Constants.ENERGY_LEVELS - 1