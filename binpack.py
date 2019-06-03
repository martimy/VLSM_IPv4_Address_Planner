
BIN_SIZE = 20

def find_first_bin(req, slack):
    b = 0
    while b < len(slack):
        if req <= slack[b]:
            break
        b += 1

    if b == len(slack):
        slack.append(BIN_SIZE)

    slack[b] -= req
    return b

def find_best_bin(req, slack):
    best = 2**32-1
    b = 0
    c = 0
    while c < len(slack):
        if (req <= slack[c]) and (slack[c] < best):
            best = slack[c]
            b = c
        c += 1

    if c == len(slack):
        slack.append(BIN_SIZE)

    slack[b] -= req
    return b


if __name__ == '__main__':

    term = [7, 2, 6, 5, 2, 6, 9, 3]
    sorted_term = sorted(term, reverse=True)
    sorted_idx = sorted(range(len(term)), key=lambda k: term[k], reverse=True)

    print("term  =",term)
    print("sorted=",sorted_term)
    print("idx   =",sorted_idx)

    slack1 = [BIN_SIZE]
    bins1 = [find_first_bin(term[j], slack1) for j in sorted_idx]
    print("bin1  =",bins1)

    slack2 = [BIN_SIZE]
    bins2 = [find_best_bin(term[j], slack2) for j in sorted_idx]
    print("bin2  =", bins2)
