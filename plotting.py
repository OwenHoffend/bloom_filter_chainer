import matplotlib.pyplot as plt
import numpy as np
from bloom import *
from kbounds import k_bounds

def plot_query(q, color='b'):
    x, y = q.xy_coords()
    plt.scatter(x, y, s=10, color=color)
    plt.xlabel("Reference Position")
    plt.ylabel("Query Position")
    plt.title("Reference position vs Query Position")

def plot_bloom3(q):
    filtered = f_bloom_ord3(q, 200, 1000, 5000, 0.1, 0.1, 0.1, 0)
    plot_query(filtered[3], color='blue')
    plot_query(filtered[2], color='deepskyblue')
    plot_query(filtered[1], color='lightgreen')
    plot_query(filtered[0], color='red')
    plt.show() 

def plot_bloom2(q):
    filtered = f_bloom_ord2(q, 1000, 5000, 0.1, 0.1, 0)
    plot_query(filtered[2], color='blue')
    plot_query(filtered[1], color='deepskyblue')
    plot_query(filtered[0], color='red')
    plt.show()

def plot_bloom1(q):
    filtered = f_bloom_ord1(q, 5000, 0.1, 0)
    plot_query(filtered[1], color='blue')
    plot_query(filtered[0], color='red')
    plt.show()

def plot_kbounds(q):
    filtered = f_bloom_ord2(q, 1000, 5000, 0.1, 0.1, 0)
    bounded = k_bounds(q, filtered[0], 10, 10)
    plot_query(bounded[0])
    plt.show()

#Function wrapper for misc testing
def sandbox():
    import load_anchors as la
    import os
    queries = la.load_anchors("./minimap2/test/c_eleganc.txt", readall=False, max_quers=1)
    plot_kbounds(queries)

if __name__ == "__main__":
    sandbox()