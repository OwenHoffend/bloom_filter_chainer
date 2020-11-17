import numpy as np
from load_anchors import AnchorList
from bloom_filter import BloomFilter

#Return some information about the bloom filter that is created with
#max_elements=sz and error_rate=err
def bloom_stats(sz, err):
    bf = BloomFilter(max_elements=sz, error_rate=err)
    return {"m": bf.num_bits_m, "k": bf.num_probes_k}

def f_bloom_ord1(al, sz, err, shift):
    bf = BloomFilter(max_elements=sz, error_rate=err)

    priority0 = AnchorList()
    priority1 = AnchorList() 

    for x, y in al.anchors():
        d = str((((x - y) >> shift) << shift))
        if d in bf:
            priority1.p.append((x, y))
        else:
            bf.add(d)
            priority0.p.append((x, y))
    return (priority1, priority0)

def f_bloom_ord2(al, sz1, sz2, err1, err2, shift):
    bf1 = BloomFilter(max_elements=sz1, error_rate=err1)
    bf2 = BloomFilter(max_elements=sz2, error_rate=err2)

    priority0 = AnchorList()
    priority1 = AnchorList()
    priority2 = AnchorList()

    for x, y in al.anchors():
        d = str((((x - y) >> shift) << shift))
        if d in bf1:
            priority2.p.append((x, y))
        elif d in bf2:
            bf1.add(d)
            priority1.p.append((x, y))
        else:
            bf2.add(d)
            priority0.p.append((x, y))

    return (priority2, priority1, priority0)

def f_bloom_ord3(al, sz1, sz2, sz3, err1, err2, err3, shift):
    bf1 = BloomFilter(max_elements=sz1, error_rate=err1)
    bf2 = BloomFilter(max_elements=sz2, error_rate=err2)
    bf3 = BloomFilter(max_elements=sz3, error_rate=err3)

    priority0 = AnchorList()
    priority1 = AnchorList()
    priority2 = AnchorList()
    priority3 = AnchorList()

    for x, y in al.anchors():
        d = str((((x - y) >> shift) << shift))
        if d in bf1:
            priority3.p.append((x, y))
        elif d in bf2:
            bf1.add(d)
            priority2.p.append((x, y))
        elif d in bf3:
            bf2.add(d)
            priority1.p.append((x, y))
        else:
            bf3.add(d)
            priority0.p.append((x, y))

    return (priority3, priority2, priority1, priority0)

#Second-pass variants of the first and second order bloom filters
def f_bloom_ord1_2pass(al, sz, err, shift):
    hp_pass1, lp_pass1 = f_bloom_ord1(al, sz, err, shift)
    hp_pass1.merge(lp_pass1.p) #Merge such that high-priority entries are seen by the filter first
    return f_bloom_ord1(hp_pass1, sz, err, shift)

def f_bloom_ord2_2pass(al, sz1, sz2, err1, err2, shift):
    hp_pass1, mp_pass1, lp_pass1 = f_bloom_ord2(al, sz1, sz2, err1, err2, shift)
    mp_pass1.merge(lp_pass1.p)
    hp_pass1.merge(mp_pass1.p)
    return f_bloom_ord2(hp_pass1, sz1, sz2, err1, err2, shift)