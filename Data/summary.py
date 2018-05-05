#!/usr/bin/env python3

import csv
import pprint

import numpy as np

import matplotlib.pyplot as plt

pprint = pprint.PrettyPrinter(indent=4).pprint

_ASSET_DIR = '../assets/'

_CSV_FILE = './data.csv'

_ANSWERS = np.array([
    0.5102326845480449, 0.06752455312177218, #go1.X
    0.5466307162126456, 0.13793529249472486, #go1.Y
    0.36143501958470536, 0.11663910446864723, #gc1.X
    0.6846403709047718, 0.1310070042079945, #gc1.Y
    0.3442593798689419, 0.07798668256561439,
    0.5541702024123037, 0.0928575492106504,
    0.4789155103309395, 0.058228722482961265,
    0.4313900867417344, 0.12566913063737445,
    0.593417741302134, 0.14259362358115227,
    0.36907910982176023, 0.08759075972828917,
    0.5087723070686012, 0.09194877672170942,
    0.3449233640227923, 0.13638798747151842,
])

def describe(errorline):
    avg_ov_x_mean_error = (errorline[0] + errorline[8] + errorline[16]) / 3
    avg_ov_y_mean_error = (errorline[2] + errorline[10] + errorline[18]) / 3
    avg_ov_x_std_error = (errorline[1] + errorline[9] + errorline[17]) / 3
    avg_ov_y_std_error = (errorline[3] + errorline[11] + errorline[19]) / 3
    avg_co_x_mean_error = (errorline[4] + errorline[12] + errorline[20]) / 3
    avg_co_y_mean_error = (errorline[6] + errorline[14] + errorline[22]) / 3
    avg_co_x_std_error = (errorline[5] + errorline[11] + errorline[21]) / 3
    avg_co_y_std_error = (errorline[7] + errorline[13] + errorline[23]) / 3
    return {
        'overlay' : {
            'meanx' : avg_ov_x_mean_error,
            'meany' : avg_ov_y_mean_error,
            'stdx' : avg_ov_x_std_error,
            'stdy' : avg_ov_y_std_error,
        },
        'coordinate' : {
            'meanx' : avg_co_x_mean_error,
            'meany' : avg_co_y_mean_error,
            'stdx' : avg_co_x_std_error,
            'stdy' : avg_co_y_std_error,
        }
    }


def process(data):
    def fix(d, k):
        if d['overlay'][k] > d['coordinate'][k]:
            return (d['coordinate'][k] - d['overlay'][k]) / d['coordinate'][k]
        else:
            return (d['coordinate'][k] - d['overlay'][k]) / d['overlay'][k]
        
    return [
        {
            k : d['coordinate'][k] - d['overlay'][k]
            for k in ['meanx', 'meany', 'stdx', 'stdy']
        }
        for d in data
    ]


if __name__ == '__main__':

    DATA = []

    with open(_CSV_FILE, 'rU') as csvfile:
        r = list(csv.reader(csvfile))[1:]
        for line in r:
            d = np.array([float(x) for x in line[1:]])
            # E = (estimate - actual)
            error = np.absolute(np.subtract(d, _ANSWERS))
            DATA.append(describe(error))

    print([d['overlay']['meanx'] for d in DATA])

    ind = np.arange(4)
    labels = ['meanx', 'meany', 'stdx', 'stdy']
    ticks = ['$\mu_{x}$', '$\mu_{y}$', '$\sigma_{x}$', '$\sigma_{y}$']

    pprint(DATA)
    print()
    pprint(process(DATA))
    data = [sum([d[k] for d in process(DATA)])/6 for k in labels]
    print()
    pprint(data)

    f, ax = plt.subplots()

    r1 = ax.bar(ind, data, color='blue', tick_label=ticks)

    ax.set_ylabel('Error (Coordinate) - Error (Overlay)')
    ax.set_title('Comparison of Error by Plot Type')
    ax.axhline(y=0, color="black")
    plt.show()
