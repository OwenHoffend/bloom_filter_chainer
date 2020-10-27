from bloom_filter import BloomFilter

#Return some information about the bloom filter that is created with
#max_elements=sz and error_rate=err
def bloom_stats(sz, err):
    bf = BloomFilter(max_elements=sz, error_rate=err)
    return {"m": bf.num_bits_m, "k": bf.num_probes_k}

def f_bloom_ord1(ql, sz, err, shift):
    bf = BloomFilter(max_elements=sz, error_rate=err)

    priority0 = AnchorList()
    priority1 = AnchorList() 

    for x, y in ql.anchors():
        d = (((x - y) >> shift) << shift)
        if d in bf:
            priority1.p.append((x, y))
        else:
            bf.add(d)
            priority0.p.append((x, y))
    return (priority1, priority0)

def f_bloom_ord2(ql, sz1, sz2, err1, err2, shift):
    bf1 = BloomFilter(max_elements=sz1, error_rate=err1)
    bf2 = BloomFilter(max_elements=sz2, error_rate=err2)

    priority0 = AnchorList()
    priority1 = AnchorList()
    priority2 = AnchorList()

    for x, y in ql.anchors():
        d = (((x - y) >> shift) << shift)
        if d in bf1:
            priority2.p.append((x, y))
        elif d in bf2:
            bf1.add(d)
            priority1.p.append((x, y))
        else:
            bf2.add(d)
            priority0.p.append((x, y))

    return (priority2, priority1, priority0)

#Starting point: Make 2nd-pass variants of these functions for testing purposes