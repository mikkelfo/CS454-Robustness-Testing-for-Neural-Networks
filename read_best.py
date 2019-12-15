import pickle
from mask import Mask

read = open('best_mask', 'rb')
best_mask = pickle.load(read)
read.close()

print("best mask fitness: ", best_mask.fitness)
print("best mask accuracy: ", best_mask.accuracy)
print("best mask change: ", best_mask.change)
