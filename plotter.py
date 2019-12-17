import matplotlib.pyplot as plt
import pickle
from mask import Mask

read = open('results\pop150\shapes_20_diff_30\pareto_pop', 'rb')
population = pickle.load(read)
read.close()

new_population = []
for i in population:
    append = True
    for j in population:
        if (i.accuracy > j.accuracy and i.change > j.change):
            append = False
    if (append):
        new_population.append(i)
    
xAccuracy = []
yChange = []
for ind in new_population:
    xAccuracy.append(ind.accuracy)
    yChange.append(ind.change)

print(xAccuracy)
print(yChange)

plt.scatter(yChange, xAccuracy,label="mask", color="black", marker="*", s=30)
plt.xlabel("Change")
plt.ylabel("Accuracy")
plt.title("Pareto Population")
plt.legend()

plt.show()
plt.savefig("temp.png")

dumpLog = open('dump_log', 'wb')
pickle.dump([xAccuracy, yChange], dumpLog, -1)
dumpLog.close()
