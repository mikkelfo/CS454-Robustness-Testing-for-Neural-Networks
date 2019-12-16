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

plt.scatter(xAccuracy, yChange, label="mask", color="black", marker="*", s=30)
plt.xlabel("Accuracy")
plt.ylable("Change")
plt.title("Pareto Population - 100, 40, 9")
plt.legend()

plt.show
