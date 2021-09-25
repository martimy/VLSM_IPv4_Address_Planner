class BinPack(object):

    def __init__(self, bins, bin_size):
        self.BINS = bins
        self.BIN_SIZE = bin_size


    def fit_old(self, req, type="FIRST"):
        # sort the requirements in decreasing order and return the index
        sorted_idx = sorted(range(len(req)), key=lambda k: req[k], reverse=True)
        print(sorted_idx)
        self.slack = [self.BIN_SIZE] * self.BINS

        if type == "BEST":
            fitted = [self.__find_best_bin(req[j]) for j in sorted_idx]
        elif type == "WORST":
            fitted = [self.__find_worst_bin(req[j]) for j in sorted_idx]
        else: # FIRST
            fitted = [self.__find_first_bin(req[j]) for j in sorted_idx]

        if None not in fitted:
            original_order = [0] * len(sorted_idx)
            for i in range(len(sorted_idx)):
                original_order[sorted_idx[i]] = fitted[i]
            return [k[0] * self.BIN_SIZE + k[1] for k in original_order], original_order
        return None
    
    def fit(self, req, type="FIRST"):
        self.slack = [self.BIN_SIZE] * self.BINS

        if type == "BEST":
            fitted = [self.__find_best_bin(r) for r in req]
        elif type == "WORST":
            fitted = [self.__find_worst_bin(r) for r in req]
        else: # FIRST
            fitted = [self.__find_first_bin(r) for r in req]

        return fitted

    def __find_first_bin(self, req):
        # Search bins until one that can accomodate the requirements is found.
        
        b = 0
        while b < self.BINS and req > self.slack[b]:
            b += 1
    
        # Return if no bin is found
        if b == self.BINS:
            return None
    
        # Update the remaining space
        c = self.BIN_SIZE - self.slack[b]
        self.slack[b] -= req
        
        # return the bin number and the starting position of space used
        return b, c
    
    def __find_best_bin(self, req):
        # Search bins until one that can accomodate the requirements
        # while leaving minimum space is found.
        
        best = 4294967295  # any large number
        b = -1
        for i in range(self.BINS):
            if (req <= self.slack[i]) and (self.slack[i] < best):
                best = self.slack[i]
                b = i
    
        if b == -1:
            return None
    
        c = self.BIN_SIZE - self.slack[b]
        self.slack[b] -= req
        return b, c
    
    def __find_worst_bin(self, req):
        # Search bins until one that can accomodate the requirements
        # while leaving maximum space is found.

        best = 0
        b = -1
        for i in range(self.BINS):
            if (req <= self.slack[i]) and (self.slack[i] > best):
                best = self.slack[i]
                b = i
    
        if b == -1:
            return None
    
        c = self.BIN_SIZE - self.slack[b]
        self.slack[b] -= req
        return b, c

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

