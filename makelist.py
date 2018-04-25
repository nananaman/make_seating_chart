import random

f = open('list.txt', mode='w')
for i in range(60):
    n = random.randint(1, 1000)
    f.write('hoge' + str(n) + '\n')
f.close() 

