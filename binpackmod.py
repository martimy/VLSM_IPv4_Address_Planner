class BinPack(object):

    def __init__(self, bins, bin_size):
        self.BINS = bins
        self.BIN_SIZE = bin_size


    def fit(self, req, type="FIRST"):
        # sort the requirements in decreasing order and return the index
        sorted_idx = sorted(range(len(req)), key=lambda k: req[k], reverse=True)
        self.slack = [self.BIN_SIZE] * self.BINS

        if type == "BEST":
            fitted = [self.__find_best_bin(req[j]) for j in sorted_idx]
        elif type == "WORST":
            fitted = [self.__find_worst_bin(req[j]) for j in sorted_idx]
        else: # FIRST
            fitted = [self.__find_first_bin(req[j]) for j in sorted_idx]

        if not (None in fitted):
            original_order = [0] * len(sorted_idx)
            for i in range(len(sorted_idx)):
                original_order[sorted_idx[i]] = fitted[i]
            return [k[0] * self.BIN_SIZE + k[1] for k in original_order], original_order
        return None

    def __find_first_bin(self, req):
        b = 0
        while b < self.BINS and req > self.slack[b]:
            b += 1
    
        if b == self.BINS:
            return None
    
        c = self.BIN_SIZE - self.slack[b]
        self.slack[b] -= req
        return b, c
    
    def __find_best_bin(self, req):
        best = 2**32-1
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
    print(term)

    bins = BinPack(4, 20)
    result1, fit1 = bins.fit(term)
    print(result1)
    print(fit1)

    result2, fit2 = bins.fit(term, type="BEST")
    print(result2)
    print(fit2)

    result3, fit3 = bins.fit(term, type="WORST")
    print(result3)
    print(fit3)

