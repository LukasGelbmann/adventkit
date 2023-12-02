def solve(data):
    binarized_data = data.translate(str.maketrans("FBLR", "0101"))
    seat_ids = {int(line, base=2) for line in binarized_data.splitlines()}
    print(max(seat_ids))
    print(missing(seat_ids))


def missing(seat_ids):
    i = min(seat_ids)
    while i in seat_ids:
        i += 1
    return i
