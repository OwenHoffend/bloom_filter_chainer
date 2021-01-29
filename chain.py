import math, statistics

#Where does w and w_avg come from, exactly? I think I might need to export this
def chain(anchors, w_vals):
    w_avg = statistics.mean(w_vals)
    f = [-math.inf for _ in range(len(anchors))]
    for i in range(len(anchors)):
        max_score = -math.inf
        for j in range(i):
            dx = anchors[i].x - anchors[j].x
            dy = anchors[i].y - anchors[j].y
            alpha = min(min(dy, dx), w_vals[i])
            beta  = mm2_gap_cost(dy - dx, w_avg)
            new_score = f[j] + alpha - beta
            if new_score > max_score:
                max_score = new_score
        f[i] = max(max_score, w_vals[i])
    return f

def mm2_gap_cost(l, w_avg):
    if l == 0:
        return 0
    else:
        abs_l = abs(l)
        return 0.01 * w_avg * abs_l + 0.5 * math.log(abs_l, 2)

#Testing
def test_chain():
    pass
    #import load_anchors as la
    #test_anchors = la.load_query_at("./minimap2/test/c_eleganc.txt", 1)
    #scores = chain(test_anchors, )

if __name__ == "__main__":
    test_chain()