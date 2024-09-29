import random

loop_cnt =10000

freq = [170, 139, 100, 41, 37, 23, 37, 15, 40, 29, 35, 17, 24, 18, 160, 45, 35, 140]
occur = [0 for _ in freq]
for _ in range(loop_cnt):
    r = random.randint(0, 950)
    coll = []
    for i, v in enumerate(freq):
        if r % v == 0:
            occur[i] += 1
            coll.append(v)
    # if len(coll) >1:
    #     print("collison: {} {}".format(
    #         r, ','.join(map(str,coll))
    #     ))

print(occur)
print([f"{x/loop_cnt*100}%" for x in occur])
print(sum(occur) / loop_cnt)

"""
[64, 76, 86, 247, 268, 452, 268, 681, 257, 347, 291, 561, 452, 607, 58, 230, 291, 59]
['0.64%', '0.76%', '0.86%', '2.4699999999999998%', '2.68%', '4.52%', '2.68%', '6.81%', '2.5700000000000003%', '3.47%', '2.91%', '5.609999999999999%', '4.52%', '6.069999999999999%', '0.58%', '2.3%', '2.91%', '0.59%']
0.5295
"""

conditions = [-1, 0, 0, 0]
for _ in range(loop_cnt*100):
    randoms = [random.randint(0, 7) for _ in range(3)]
    conditions[len(set(randoms))] += 1

print(conditions)
