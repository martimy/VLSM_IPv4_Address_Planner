# =============================================================================
# Copyright 2022 Maen Artimy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

"""
A BinPack algorithm form address planner
"""


class BinPack():
    """
    performs bin packing
    """

    def __init__(self, bins, bin_size):
        self.bins = bins
        self.bin_size = bin_size
        self.slack = []

    def fit(self, req, pack_type="FIRST"):
        """
        fits requirements in bins based on packing type.
        """

        self.slack = [self.bin_size] * self.bins

        if pack_type == "BEST":
            fitted = [self.find_best_bin(r) for r in req]
        elif pack_type == "WORST":
            fitted = [self.find_worst_bin(r) for r in req]
        else:  # FIRST
            fitted = [self.find_first_bin(r) for r in req]

        return fitted

    def find_first_bin(self, req):
        """
        Find the first bin the has enough slack to fit the requirements
        """

        bin_number = 0
        while bin_number < self.bins and req > self.slack[bin_number]:
            bin_number += 1

        # Return if no bin is found
        if bin_number == self.bins:
            return None

        # Update the remaining space
        start_position = self.bin_size - self.slack[bin_number]
        self.slack[bin_number] -= req

        # return the bin number and the starting position of space used
        return bin_number, start_position

    def find_best_bin(self, req):
        """
        Finds the first bin can accomodates the requirements
        while leaving minimum space.
        """

        best = 4294967295  # any large number
        bin_number = -1
        for i in range(self.bins):
            if (req <= self.slack[i]) and (self.slack[i] < best):
                best = self.slack[i]
                bin_number = i

        if bin_number == -1:
            return None

        start_position = self.bin_size - self.slack[bin_number]
        self.slack[bin_number] -= req
        return bin_number, start_position

    def find_worst_bin(self, req):
        """
        Find the first bin that can accomodate the requirements
        while leaving maximum space.
        """

        worst = 0
        bin_number = -1
        for i in range(self.bins):
            if (req <= self.slack[i]) and (self.slack[i] > worst):
                worst = self.slack[i]
                bin_number = i

        if bin_number == -1:
            return None

        start_position = self.bin_size - self.slack[bin_number]
        self.slack[bin_number] -= req
        return bin_number, start_position


if __name__ == '__main__':

    term = [7, 2, 6, 5, 2, 6, 9, 3]
    # term = [16, 4, 1]
    print(term)

    binset = BinPack(4, 20)
    # bins = BinPack(2, 16)
    result1 = binset.fit(term)
    print(result1)

    result2 = binset.fit(term, pack_type="BEST")
    print(result2)

    result3 = binset.fit(term, pack_type="WORST")
    print(result3)
