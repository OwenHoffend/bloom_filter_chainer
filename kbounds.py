from load_anchors import AnchorList

def find_primary_ds(al_filtered, num_top, alltop=False, run_until=10, shift=0, get_size=False):
    ht = {}
    max_keys = [0, ]
    max_cnts = [1,]
    for x, y in al_filtered.anchors():
        d = x - y
        key = str(((d >> shift) << shift))
        if key in ht:
            ht[key] += 1
            cnt = ht[key]
            for i, mcnt in enumerate(max_cnts):
                if cnt > mcnt:
                    max_cnts[i] = cnt
                    max_keys[i] = int(key)
                    if mcnt >= run_until:
                        print("HT Size: {}".format(len(ht.keys())))
                        if get_size:
                            return len(ht.keys())
                        else:
                            return max_keys
                    break
            else:
                if len(max_cnts) < num_top or (alltop and cnt > 1):
                    max_cnts.append(cnt)
                    max_keys.append(int(key))
        else:
            ht[key] = 1
    print("HT Size: {}".format(len(ht.keys())))
    if get_size:
        return len(ht.keys())
    else:
        return max_keys

def k_bounds(al, al_filtered, k_dist, num_top, alltop=False, run_until=10, shift=0):
    primary_ds = find_primary_ds(al_filtered, num_top, alltop, run_until=run_until, shift=shift)
    priority0 = AnchorList()
    priority1 = AnchorList()
    for x, y in al.anchors():
        d = x - y
        for pd in primary_ds:
            if abs(d - pd) < k_dist:
                priority1.p.append((x, y))
                break
        else:
            priority0.p.append((x, y))

    return (priority1, priority0)