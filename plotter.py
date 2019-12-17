import matplotlib.pyplot as plt
import pickle
from mask import Mask

#read population
read = open('pareto_pop', 'rb')
population = pickle.load(read)
read.close()

#filter out dominated masks not dominated during the run
new_population = []
for i in population:
    append = True
    for j in population:
        if (i.accuracy > j.accuracy and i.change > j.change):
            append = False
    if (append):
        new_population.append(i)

#read out for plotting
xAccuracy = []
yChange = []
for ind in new_population:
    xAccuracy.append(ind.accuracy)
    yChange.append(ind.change)

#plot pareto front
plt.scatter(yChange, xAccuracy,label="mask", color="black", marker="*", s=30)
plt.xlabel("Change")
plt.ylabel("Accuracy")
plt.title("Pareto Population")
plt.legend()
plt.show()
plt.savefig("pareto_graph.png")