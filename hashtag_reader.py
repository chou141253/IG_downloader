import os
import json

def read():
    with open("instagram_rank.json", "r") as fjson:
        ranks = json.load(fjson)
    return ranks

# for test
if __name__ == "__main__":
    ranks = read()
    for r in ranks:
        print(r, ranks[r])


