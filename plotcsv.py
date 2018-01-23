#!/usr/bin/env python3
import argparse
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description='Plot text file')
    parser.add_argument('filename', nargs='+',
                        help='list of files to check (default: *)')
    parser.add_argument('xcolumn', nargs='?', type=int, default=0,
                        help='Column number for x axis')
    parser.add_argument('ycolumn', nargs='?', type=int, default=1,
                        help='Column number for y axis')
    args = parser.parse_args()

    data = pd.read_csv(args.filename, delim_whitespace=True, header=None)
    fig, ax = plt.subplots(1, 1, sharey=True, figsize=(6, 4), tight_layout={"pad": 0.3, "w_pad": 0.0, "h_pad": 0.0})

    ax.plot(data.iloc[:, args.xcolumn], data.iloc[:, args.ycolumn], marker="None", lw=1.5, color='black')

    # ax.set_xlabel(r'Electron energy [eV]', fontsize=fs)
    # ax.set_ylabel(r'y(E)', fontsize=fs)
    outputfilename = args.filename + '.pdf'
    print(f"Saving '{outputfilename}'")
    fig.savefig(outputfilename, format='pdf')
    plt.close()


if __name__ == "__main__":
    main()
