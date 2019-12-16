import matplotlib.pyplot as plt
import pickle
from mask import Mask

read = open('pareto_pop', 'rb')
population = pickle.load(read)
read.close()

xAccuracy = []
yChange = []
for ind in population:
    xAccuracy.append(ind.accuracy)
    yChange.append(ind.change)

print(xAccuracy)
print(yChange)

plt.scatter(xAccuracy, yChange, label="mask", color="black", marker="*", s=30)
plt.xlabel("Accuracy")
plt.ylabel("Change")
plt.title("Pareto Population - 100, 40, 9")
plt.legend()

plt.show()
plt.savefig("temp.png")

dumpLog = open('dump_log', 'wb')
pickle.dump([xAccuracy, yChange], dumpLog, -1)
dumpLog.close()
