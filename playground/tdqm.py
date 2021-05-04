# from tqdm.auto import trange
# from time import sleep
#
# for i in trange(4, desc='1st loop'):
#     for j in trange(5, desc='2nd loop'):
#         for k in trange(50, desc='3rd loop', leave=False):
#             sleep(0.01)

import random

i_map = {0: "first", 1: "second", 2: "third"}
for i in range(3):
    count = 0
    result = []
    for _ in range(99):
        r = random.randint(0, 1)
        result.append(r)
        count = count + random.randint(0, 1)

    print(result)
    # print(len(result))
    print(count)
    decide = " NO GO"
    if count >= 5:
        decide = " GO"
    print("{} time random result is :{}".format(i_map[i], decide))
