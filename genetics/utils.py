"""
"Beacon" (c) by Ignacio Slater M.
"Beacon" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import random
from copy import copy
from typing import List


def generate_cut_points(self, other) -> List[int]:
    max_cuts = min(self.__len__(), other.__len__())
    number_of_cuts = random.randint(0, max_cuts)  # Choose a random number of cut points
    mixing_points = [random.randint(0, max_cuts) for _ in range(0, number_of_cuts)]
    mixing_points.sort()
    return mixing_points


def create_offsprings(self, other):
    cut_points = generate_cut_points(self, other)
    offsprings = (self.__copy__(), other.__copy__())
    i = 0
    start = 0
    while i < len(cut_points):  # While there's still cut points left
        end = cut_points[i]
        for index in range(start, end):
            offsprings[0][index] = copy(other.genotype[index] if i % 2 == 0
                                        else self.genotype[index])
            offsprings[1][index] = copy(self.genotype[index] if i % 2 == 0
                                        else other.genotype[index])
        start = end
        i += 1
    return offsprings
