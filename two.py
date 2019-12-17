import GA
import fitnessfunction
import edit_images as editor
import random
import pickle
import copy


populationSize = 100
imageSize = 299
crossoverRate = 0.9
mutationRate = 0.1
# evaluation budget = population size + generations required
evaluationBudget = populationSize + 500

#download model if necessary
download = False
if download:
    fitnessfunction.download_base_model()

#get model, images, label
inception = fitnessfunction.load_model()
original_images = fitnessfunction.get_images()
labels = fitnessfunction.get_labels()

# get the original accuracy (no masks applied)
original_accuracy = fitnessfunction.fitness_value(
    inception, original_images, labels)
print("Original Accuracy: " + f"{original_accuracy:e}")

# initialise empty mask population
population = GA.init_population(populationSize)

# evaluate/update first generation
for i in range(0, len(population)):
    print("running update: " + str(i))
    population[i].update(inception, editor.apply_mask(
        copy.deepcopy(original_images), population[i]), labels, original_accuracy)
    print("Fitness: " + f"{population[i].fitness:e}")  # <- sci-notation
    print("Change of the mask: %8.3f Number of shapes in the mask: %d" %
          (population[i].change, len(population[i].shapes)))
    evaluationBudget -= 1

#get 1 new child from random parents
    generation = 1
while evaluationBudget > 0:
    new_pop = []
    selection = []
    if (len(population) >= 2):
        selection = random.sample(population, 2)
    else:
        selction = population.append(population[0])
    for i in range(0, len(selection), 2):
        if random.random() < crossoverRate:
            childMask = GA.crossover(selection[i], selection[i + 1])
        else:
            childMask = selection[0]
        for shape in childMask.shapes:
            if random.random() < mutationRate:
                GA.mutation(shape)
            shape.update()
        new_pop.append(childMask)

    for i in range(0, len(new_pop)):
        new_pop[i].update(inception, editor.apply_mask(
            copy.deepcopy(original_images), new_pop[i]), labels, original_accuracy)
        print("Fitness: " + f"{new_pop[i].fitness:e}")  # <- sci-notation
        print("Change of the mask: %8.3f Number of shapes in the mask: %d" %
              (new_pop[i].change, len(new_pop[i].shapes)))
        evaluationBudget -= 1

    #compare new child with poulation
    if (new_pop):
        comparable = True
        dominator = False
        for i in range(0, len(population)):
            if (population[i].accuracy > new_pop[0].accuracy and population[i].change > new_pop[0].change):
                comparable = False
                dominator = True
                break
            else:
                if (population[i].accuracy < new_pop[0].accuracy and population[i].change < new_pop[0].change):
                    comparable = False
        if (dominator):
            print("dominator")
            population = [x for x in population if not (
                new_pop[0].accuracy < x.accuracy and new_pop[0].change < x.change)]
            population.append(new_pop[0])
        if (comparable):
            population.append(new_pop[0])
            print("comparable")

    print("End Generation " + str(generation) +
          " with population of:" + str(len(population)))
    generation += 1

    # open file for pareto population
    with open('pareto_pop', 'wb') as output:
        pickle.dump(population, output, -1)