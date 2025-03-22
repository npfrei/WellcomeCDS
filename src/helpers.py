import csv
import matplotlib.pyplot as plt
from collections import OrderedDict
import json


def write_dict_to_csv(file_path, _dict):
    # Write a dict to a csv
    # https://stackoverflow.com/questions/8685809/writing-a-dictionary-to-a-csv-file-with-one-line-for-every-key-value
    with open(file_name, "w", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        for key, value in _dict.items():
            writer.writerow([key, value])


def plot_dict_from_csv(file, xlabel, ylabel, ytype: type, xtype: type, min_row_value, plotf):
    ## Plot a dictionary read from a csv (I guess?)
    xy = OrderedDict()
    with open(file, "r", encoding="utf-8") as csvfile:
        plots = csv.reader(csvfile, delimiter=",")
        xy = {
            ytype(row[1]): xtype(row[0])
            for row in plots
            if row and ytype(row[1]) > min_row_value
        }

    x, y = zip(*xy.items())

    plotf(x, y, color="g", label=ylabel)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=70)
    plt.legend()
    plt.show()
