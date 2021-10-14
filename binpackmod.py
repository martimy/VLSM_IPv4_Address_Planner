class BinPack(object):

    def __init__(self, bins, bin_size):
        self.BINS = bins
        self.BIN_SIZE = bin_size

    def fit(self, req, type="FIRST"):
        self.slack = [self.BIN_SIZE] * self.BINS
        
        if type == "BEST":
            fitted = [self.find_best_bin(r) for r in req]
        elif type == "WORST":
            fitted = [self.find_worst_bin(r) for r in req]
        else: # FIRST
            fitted = [self.find_first_bin(r) for r in req]

        return fitted
    
    def find_first_bin(self, req):
        # Find the first bin the has enough slack to fit the requirements
        
        bin_number = 0
        while bin_number < self.BINS and req > self.slack[bin_number]:
            bin_number += 1
    
        # Return if no bin is found
        if bin_number == self.BINS:
            return None
        
        # Update the remaining space
        start_position = self.BIN_SIZE - self.slack[bin_number]
        self.slack[bin_number] -= req

        # return the bin number and the starting position of space used
        return bin_number, start_position            

    
    def find_best_bin(self, req):
        # Search bins until one that can accomodate the requirements
        # while leaving minimum space is found.
        
        best = 4294967295  # any large number
        bin_number = -1
        for i in range(self.BINS):
            if (req <= self.slack[i]) and (self.slack[i] < best):
                best = self.slack[i]
                bin_number = i
    
        if bin_number == -1:
            return None
    
        start_position = self.BIN_SIZE - self.slack[bin_number]
        self.slack[bin_number] -= req
        return bin_number, start_position
    
    def find_worst_bin(self, req):
        # Search bins until one that can accomodate the requirements
        # while leaving maximum space is found.

        worst = 0
        bin_number = -1
        for i in range(self.BINS):
            if (req <= self.slack[i]) and (self.slack[i] > worst):
                worst = self.slack[i]
                bin_number = i
    
        if bin_number == -1:
            return None
    
        start_position = self.BIN_SIZE - self.slack[bin_number]
        self.slack[bin_number] -= req
        return bin_number, start_position

if __name__ == '__main__':
    
    term = [7, 2, 6, 5, 2, 6, 9, 3]
    # term = [16, 4, 1]
    print(term)

    bins = BinPack(4, 20)
    # bins = BinPack(2, 16)
    result1 = bins.fit(term)
    print(result1)

    result2 = bins.fit(term, type="BEST")
    print(result2)
    
    result3 = bins.fit(term, type="WORST")
    print(result3)

