import json
import matplotlib.pyplot as plt
import pandas as pd
from collections import OrderedDict
import jenkspy
import timeit
import random


def plot(d):
    plotter = pd.DataFrame(d.items(), columns=["count", "edit_count"])

    ax = plt.gca()
    plotter.plot(kind="line", x="count", y="edit_count", ax=ax)

    plt.show()


def jenks_natural_breaks(d):
    arr = list(d.values())
    jenks = jenkspy.jenks_breaks(arr, nb_class=4)

    print(jenks)


def jenks_tester():
    list_of_values = [random.random() * 5000 for _ in range(500000)]
    breaks = jenkspy.jenks_breaks(list_of_values, nb_class=6)
    print(breaks)


def find_users(d, i):
    users = []
    for key, value in d.items():
        if value > i:
            users.append(key)
    print(len(users))
    return users


def main():
    with open(
        "/Volumes/KINGSTON/txtlab/may-21/editors_all.json",
        encoding="utf-8",
        errors="ignore",
    ) as json_data:
        d = json.load(json_data)

    d_sorted = OrderedDict(sorted(d.items(), key=lambda x: x[1]))

    jenks_natural_breaks(d_sorted)

    # users = find_users(d, 28)


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print("Time:", stop - start)
