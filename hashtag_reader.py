import json


def read(file):
    with open(file, "r") as fjson:
        ranks = json.load(fjson)
    return ranks


# for test
if __name__ == "__main__":
    ranks = read(file="instagram_rank.json")
    for r in ranks:
        print(r, ranks[r])
