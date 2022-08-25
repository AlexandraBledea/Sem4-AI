import csv
import math
import random
import matplotlib.pyplot as plot


class Program:

    def __init__(self):
        self._real_points = {}
        self._predicted_points = {}

        self._centroids = []
        self._min1 = 9999999999999999.99
        self._min2 = 9999999999999999.99
        self._max1 = -9999999999999999.99
        self._max2 = -9999999999999999.99

        self._counts_real = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
        self._counts_predicted = [0 for _ in range(4)]

        self._label_to_index = {'A': None, 'B': None, 'C': None, 'D': None}
        self._index_to_label = [None for _ in range(4)]

        self.read_points()
        self._initialize_centroids()

    @staticmethod
    def euclidian_distance(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def _initialize_centroids(self):
        # We "created" a minimal rectangle and not the initial centroids will be taken randomly from its inside
        for _ in range(4):
            self._centroids.append((random.uniform(self._min1, self._max1), random.uniform(self._min2, self._max2)))

    def read_points(self):
        with open('dataset.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:

                self._counts_real[row[0]] += 1

                # We are going to keep for each point the real cluster label, so basically we are going
                # to keep for every point (A, B, C or D)
                self._real_points[(float(row[1]), float(row[2]))] = row[0]

                # We are going to predict for each point a centroid index, so basically we are going
                # to keep into a dictionary, for every point (0, 1, 2 or 3)

                self._predicted_points[(float(row[1]), float(row[2]))] = None

                # Here we compute the coordinates in order to create the minimal rectangle
                self._min1 = min([self._min1, float(row[1])])
                self._min2 = min([self._min2, float(row[2])])
                self._max1 = max([self._max1, float(row[1])])
                self._max2 = max([self._max2, float(row[2])])

    def iterate(self):

        # For every real point, we are going to compute which centroid is closer to it
        for p in self._predicted_points:

            minimum_index = None
            minimum_distance = 9999999999999999.99

            for i in range(4):

                distance = Program.euclidian_distance(p, self._centroids[i])

                if distance < minimum_distance:
                    minimum_distance = distance
                    minimum_index = i

            # For each point we will store the index of the nearest centroid
            self._predicted_points[p] = minimum_index

        # We compute how many points are closest to each centroid
        self._counts_predicted = [0 for _ in range(4)]

        # We are going to sum up all the coordinates of the nearest points to each centroid in
        # Order to be able to the mean later on
        sums = [[0, 0] for _ in range(4)]

        for p in self._predicted_points:
            self._counts_predicted[self._predicted_points[p]] += 1
            sums[self._predicted_points[p]][0] += p[0]
            sums[self._predicted_points[p]][1] += p[1]

        # Now, the new centroids will be computer as the "mean" of all the nearest points to it
        for i in range(4):
            self._centroids[i] = (
                round(sums[i][0] / self._counts_predicted[i], 20), round(sums[i][1] / self._counts_predicted[i], 20))

    def _run(self, iteration_count):
        for _ in range(iteration_count):
            self.iterate()

    def _plot_all(self):
        colors = {0: "pink", 1: "blue", 2: "purple", 3: "orange"}

        for p in self._predicted_points:
            plot.scatter(p[0], p[1], color=colors[self._predicted_points[p]], marker=".", s=3)

        for index in range(4):
            plot.scatter(self._centroids[index][0], self._centroids[index][1], color=colors[index], marker="X", s=50)

        plot.show()

    def map_indexes_to_labels(self):

        matches = {}
        # This dictionary is going to hold how many label-index associations were made in total
        # there exists in total, 16 distinct possible associations, but we will only take the top 4
        # which are the most frequent ones.
        # Those will represent the most appropriate label-index mapping

        for l in self._label_to_index.keys():
            for i in range(4):
                matches[(l, i)] = 0

        for p in self._real_points.keys():
            # For each point, we take the index of the closest predicted centroid to it
            # and the real cluster label for each

            label = self._real_points[p]
            index = self._predicted_points[p]

            # For the associated label and index, we compute how many times those two
            # were associated
            matches[(label, index)] += 1

        matches_pairs = []
        for k, v in matches.items():
            matches_pairs.append((k, v))

        matches_pairs.sort(key=lambda v: v[1], reverse=True)

        # So basically, after the association is done, we take the pairs ((label, index), count) and order them by
        # the count

        results = matches_pairs[:4]

        # Now, the top 4 ones, are closest to being the correct values, or at least they are very very close

        for p in results:
            self._label_to_index[p[0][0]] = p[0][1]
            self._index_to_label[p[0][1]] = p[0][0]

    # We'll organize the guesses and the real labels in a matrix, using the label-index mapping we've made.
    def _compute_guess_matrix(self):

        self._guesses_matrix = [[0 for _ in range(4)] for _ in range(4)]

        for point in self._real_points.keys():
            true_index = self._label_to_index[self._real_points[point]]
            predicted_index = self._predicted_points[point]
            self._guesses_matrix[predicted_index][true_index] += 1

    def _compute_for_label_measurement(self, label_index):
        """
        for each label, i = label's index:
            true positives = m[i][i]
            true negatives = sum(m[j][k]), j, k != i -> the matrix without the current line and column
            false positives = sum(m[i][j]), j != i -> just the current row (without position [i][i])
            false negatives = sum(m[j][i]), j != i -> just the current column (without position [i][i])
        """
        # TP = no. of correct guesses that a certain point belongs to the current label
        true_positive = self._guesses_matrix[label_index][label_index]

        true_negative, false_positive, false_negative = 0, 0, 0

        for i in range(4):

            for j in range(4):

                if i != label_index and j != label_index:
                    # TN = Guesses that have nothing to do with the current label.
                    true_negative += self._guesses_matrix[i][j]
                elif i == label_index and j != label_index:
                    # FP = Points that were wrongly guessed as being part of the current label.
                    false_positive += self._guesses_matrix[i][j]
                elif i != label_index and j == label_index:
                    # FN = Points that should've been guessed as being part of the current label.
                    false_negative += self._guesses_matrix[i][j]

        return [true_positive, true_negative, false_positive, false_negative]

    def execute(self):

        self._run(200)
        self.map_indexes_to_labels()

        print(self._label_to_index)

        self._compute_guess_matrix()

        print(self._guesses_matrix)

        TP = 0
        TN = 0
        FP = 0
        FN = 0

        for index in range(4):
            ms = self._compute_for_label_measurement(index)
            print(ms)
            TP += ms[0]
            TN += ms[1]
            FP += ms[2]
            FN += ms[3]

        ATP = TP / 4
        ATN = TN / 4
        AFP = FP / 4
        AFN = FN / 4

        accuracy = (ATP + ATN) / (ATP + ATN + AFP + AFN)
        precision = ATP / (ATP + AFP)
        rappel = ATP / (ATP + AFN)
        score = 2 * precision * rappel / (precision + rappel)

        print("Avg. accuracy: " + str(accuracy * 100) + "%")
        print("Avg. precision: " + str(precision * 100) + "%")
        print("Avg. rappel: " + str(rappel * 100) + "%")
        print("Avg. score: " + str(score * 100) + "%")

        self._plot_all()
