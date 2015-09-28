__author__ = 'andrew'
import re
import os
writeFile = '/home/andrew/Desktop'
if not os.path.exists(writeFile):
    os.makedirs(writeFile)
g = open(os.path.join(writeFile, 'heatherNames.csv'), 'w')
f = open('stats/heather_entity_TERM_STATS_names.csv', 'r')
expression = r'([A-Z-a-z.-]+ ([A-Za-z".-]+ *[A-Za-z".-]+){1,2}$)'

NEs = []
ocount = 0
for line in f:
    ocount += 1
    line = line.split('~')
    x = re.search(expression, line[0])
    if x == None:
        continue
    else:
        NEs.append(line)
for line in NEs:
    g.write('~'.join(line))


print len(NEs)
print ocount