import matplotlib.pyplot as plt
import pickle
from mask import Mask


def load_pop():
    with open('pareto_pop', 'rb') as read:
        while True:
            try:
                yield pickle.load(read)
            except EOFError:
                break


xAccuracy = []
yChange = []
for ind in load_pop():
    xAccuracy.append(ind.accuracy)
    yChange.append(ind.change)

plt.scatter(xAccuracy, yChange, label="mask", color="black", marker="*", s=30)
plt.xlabel("Accuracy")
plt.ylable("Change")
plt.title("Pareto Population - 100, 40, 9")
plt.legend()

plt.show()

dumpLog = open('dump_log', 'wb')
pickle.dump([xAccuracy, yChange], dumpLog, -1)
dumpLog.close()
