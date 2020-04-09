import random
from operator import itemgetter

mu = 111/5
sigma = 111/5/3
dic = {}
for i in range(1, 10000):
    a = int(random.normalvariate(mu, sigma))
    # a = int(random.randint(1, 40))
    if a in dic:
        dic[a] = dic[a] + 1
    else:
        dic[a] = 1

lis = sorted(dic.items(),key=itemgetter(1),reverse=True)

for key in lis:
     print(str(key[1]) + " -> " + str(key[0]))
   # print(key)

pool = [0]*5 + [1]*95
result = [random.choice(pool) for i in range(1, 100)]
random.shuffle(result)
# print(result)

N = 1000
pool = []
result = []
for i in range(N):
    if not pool:
        pool = [0]*1 + [1]*19
    random.shuffle(pool)
    result.append(pool[-1])
    del pool[-1]


N = 10000
NN = int(N*0.05)
mu = 111/5
sigma = mu/3.
delta = [int(random.normalvariate(mu, sigma)) for i in range(NN)]
# print(delta)

a = 0
for i in delta:
    a = a + i
print(a)


