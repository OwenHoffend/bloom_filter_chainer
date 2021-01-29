import matplotlib.pyplot as plt
import numpy as np
from bloom import *
from kbounds import k_bounds, find_primary_ds

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
    for bound in range(1000, 0, -250):
        bounded = k_bounds(q, filtered[0], bound, 5, alltop=True)
        x, y = bounded[0].xy_coords()
        plt.scatter(x, y, s=10)
    plt.xlabel("Reference Position")
    plt.ylabel("Query Position")
    plt.title("Reference position vs Query Position")
    plt.show()

def plot_mem_usg(q):
    fig, ax = plt.subplots()
    #for f1_bits in range(0, 1000, 200):
    #    f_mems, ht_mems, totals = [], [], [] 
    #    for f2_bits in range(f1_bits, 10000, 100):
    #        if f1_bits != 0:
    #            f2_sz = bloom_stats(f2_bits, 0.1)["m"]
    #            f1_sz = bloom_stats(f1_bits, 0.1)["m"]
    #            filtered = f_bloom_ord2(q, f1_bits, f2_bits, 0.1, 0.1, 0)[0]
    #        else:
    #            f2_sz = 0
    #            f1_sz = 0
    #            filtered = q
    #        ht_mem = find_primary_ds(filtered, 10, get_size=True)
    #        ht_mem = float(ht_mem * 32) / 8192
    #        f_mems.append(float(f2_sz) / 8192)
    #        filter_mem = float(f1_sz + f2_sz) / 8192
    #        ht_mems.append(ht_mem)
    #        totals.append(filter_mem + ht_mem)

        #plt.scatter(f_mems, ht_mems)
    #    plt.scatter(f_mems, totals, label="Bloom filter 1 size (KB)={}".format(round(float(f1_sz) / 8192, 2)))

    f1_bits = 1000
    for r_until in range(0, 1000, 100):
        f_mems, ht_mems, totals = [], [], [] 
        for f2_bits in range(f1_bits, 10000, 100):
            if f1_bits != 0:
                f2_sz = bloom_stats(f2_bits, 0.1)["m"]
                f1_sz = bloom_stats(f1_bits, 0.1)["m"]
                filtered = f_bloom_ord2(q, f1_bits, f2_bits, 0.1, 0.1, 0)[0]
            else:
                f2_sz = 0
                f1_sz = 0
                filtered = q
            ht_mem = find_primary_ds(filtered, 10, get_size=True, run_until=r_until)
            ht_mem = float(ht_mem * 32) / 8192
            f_mems.append(float(f2_sz) / 8192)
            filter_mem = float(f1_sz + f2_sz) / 8192
            ht_mems.append(ht_mem)
            totals.append(filter_mem + ht_mem)

        #plt.scatter(f_mems, ht_mems)
        plt.scatter(f_mems, totals, label="Run until={}".format(r_until))

    plt.legend()
    plt.title("Total memory usage (KB) vs. Run until value & 2nd order bloom filter sizes")
    plt.xlabel("Bloom filter 2 size (KB)")
    plt.ylabel("Total memory usage (KB)")
    plt.show()

#Function wrapper for misc testing
def sandbox():
    import load_anchors as la
    import os

    #Normal loading and plotting of queries
    #queries = la.load_anchors("./minimap2/test/c_eleganc.txt", readall=False, max_quers=1)
    #plot_mem_usg(queries)
    #plot_kbounds(queries)

    #Loading and plotting of minimap2 chain results:
    c_eleganc_anchors = la.load_query_at("./minimap2/test/c_eleganc.txt", 5)

    filtered = f_bloom_ord2(c_eleganc_anchors, 1000, 5000, 0.1, 0.1, 0) 
    bounded = k_bounds(c_eleganc_anchors, filtered[0], 150, 4)

    x, y = bounded[0].xy_coords()
    plt.scatter(x, y, s=10)
    plt.xlabel("Reference Position")
    plt.ylabel("Query Position")
    plt.title("Reference position vs Query Position")
    #plt.show()

    c_eleganc_chain = la.load_query_at("./minimap2/test/c_eleganc_chains.txt", 5, is_chain=True, max_chains=4)
    plot_query(c_eleganc_chain, color='lightgreen')
    plt.show()

    for i in range(100):
        c_eleganc_anchors = la.load_query_at("./minimap2/test/c_eleganc.txt", i)

        filtered = f_bloom_ord2(c_eleganc_anchors, 1000, 5000, 0.1, 0.1, 0) 
        bounded = k_bounds(c_eleganc_anchors, filtered[0], 150, 4)
        c_eleganc_chain = la.load_query_at("./minimap2/test/c_eleganc_chains.txt", i, is_chain=True, max_chains=4)

if __name__ == "__main__":
    sandbox()