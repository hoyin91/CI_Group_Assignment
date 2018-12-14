import random
import numpy as np
import math
import os
import skfuzzy as fuzz
from population import Population
from individual import Individual


# Global variable setting
recombinationVar = 0.7

# Main function at here!
def main(generation_count,pop_size):
    popSize = pop_size
    pop = Population(popSize,1)
    for y in range(generation_count):
        newPop = Population(popSize,0)
        newPop.insertPopulation(pop.getFittest())
        print (pop.getFittest().getIndividualGeneArray())
        print ("Iteration: {} Fitness: {}".format(y, 1/(pop.getFittest().getFitness())))
        for x in range(int(popSize/2)):
            parent1 = FPS(pop.getPopulation())
            parent2 = FPS(pop.getPopulation())

            child1,child2 = simpleArithmeticCrossover(parent1,parent2)

            Mutation(child1,y,pop)
            Mutation(child2,y,pop)

            newPop.insertPopulation(child1)
            newPop.insertPopulation(child2)
        else:
            # replace the entire population with newly generated children
            pop = newPop
    else:
        # print out the fitness' gene array
        print (pop.getFittest().getIndividualGeneArray())

# fuzzy function
def fuzzy_system(generation_val,convergence_val):
    x_generation = np.arange(0, 1500, 50)
    x_convergence = np.arange(0, 1, 0.1)
    x_recombinationRate  = np.arange(0, 0.5, 0.1)

    # Generate fuzzy membership functions
    generation_lo = fuzz.trapmf(x_generation, [0, 0, 300,500])
    generation_md = fuzz.trimf(x_generation, [500, 750, 1000])
    generation_hi = fuzz.trapmf(x_generation, [1000, 1200, 1500,1500])
    convergence_lo = fuzz.trapmf(x_convergence, [0, 0, 0.2,0.3])
    convergence_md = fuzz.trapmf(x_convergence, [0.25, 0.4,0.6, 0.75])
    convergence_hi = fuzz.trapmf(x_convergence, [0.7, 0.8, 1,1])
    recom_lo = fuzz.trapmf(x_recombinationRate, [0, 0, 0.15,0.2])
    recom_md = fuzz.trapmf(x_recombinationRate, [0.15, 0.2, 0.3, 0.35])
    recom_hi = fuzz.trapmf(x_recombinationRate, [0.3, 0.4, 0.5,0.5])

    generation_level_lo = fuzz.interp_membership(x_generation, generation_lo, generation_val)
    generation_level_md = fuzz.interp_membership(x_generation, generation_md, generation_val)
    generation_level_hi = fuzz.interp_membership(x_generation, generation_hi, generation_val)

    convergence_level_lo = fuzz.interp_membership(x_convergence, convergence_lo, convergence_val)
    convergence_level_md = fuzz.interp_membership(x_convergence, convergence_md, convergence_val)
    convergence_level_hi = fuzz.interp_membership(x_convergence, convergence_hi, convergence_val)

    active_rule1 = np.fmax(generation_level_hi, convergence_level_hi)
    rate_activation_lo = np.fmin(active_rule1, recom_lo)

    active_rule2 = np.fmax(generation_level_md,convergence_level_md)
    rate_activation_md = np.fmin(active_rule2,recom_md)

    active_rule3 = np.fmin(generation_level_lo,convergence_level_md)
    active_rule4 = np.fmin(active_rule3, np.fmin(generation_level_lo, convergence_level_lo))
    rate_activation_hi = np.fmin(active_rule4, recom_hi)

    aggregated = np.fmax(rate_activation_lo, np.fmax(rate_activation_md, rate_activation_hi))
    recom_rate = fuzz.defuzz(x_recombinationRate, aggregated, 'centroid')

    print("recombination rate = "+str(recom_rate))
    return recom_rate

#################################
# GA algorithrm start at here
#################################

# CROSSOVER ALGORITHM #
def simpleArithmeticCrossover(parent1,parent2):
    child1 = Individual()
    child2 = Individual()

    genePosition=random.randint(0,child1.getGeneSize()-1) # take in size of gene from variable
    for x in range(child1.getGeneSize()):
        if x >= genePosition:
            geneValue1 = (recombinationVar*parent2.getIndividualGene(x)+(1-recombinationVar)*parent1.getIndividualGene(x))
            geneValue2 = (recombinationVar*parent1.getIndividualGene(x)+(1-recombinationVar)*parent2.getIndividualGene(x))
            #geneValue2 = parent1.getIndividualGene(x)
            #geneValue1 = parent2.getIndividualGene(x)
            child1.setParticularGene(x,geneValue1)
            child2.setParticularGene(x,geneValue2)
        else:
            child1.setParticularGene(x,parent1.getIndividualGene(x))
            child2.setParticularGene(x,parent2.getIndividualGene(x))

    # return both children
    return child1,child2


# MUTATION ALGORITHM
def Mutation(parent,iteration, population):
    # Init child1 as parent to undergo mutation
    child = parent
    ProbOfMutation = random.random()
    
    #c = random.uniform(0.8,1.0)

    # init mu and sigma
    mu,sigma = 0,0.1

    if iteration < 1500*0.2:
        mu, sigma = 0, 1
    elif iteration > 1500*0.2:
        mu, sigma = 0, 0.1

    for _ in range(child.getGeneSize()):
        if (ProbOfMutation > 0.05):
            print (population.getStandardDeviation(_))
            RandomgeneValue = child.getIndividualGene(_) + (random.uniform(0,2) * population.getStandardDeviation(_))
            if (RandomgeneValue < 0):
                RandomgeneValue = 0.0001
                #RandomgeneValue = float(child.selfGeneratingGene(_))
            # print ("MR: {} Gene @ {}: to geneVal: {}".format(MutationRate,_,RandomgeneValue))
            child.setParticularGene(_, RandomgeneValue)

    #print (child.getIndividualGeneArray())
    # return mutated child
    return child


# PARENT SELECTION ALGORITHM #
# return the parent based on its fitness proportional selection
def FPS(pop):
    max = sum(c.getFitness() for c in pop)
    pick = random.uniform(0, max)
    current = 0.0
    for c in pop:
        current += c.fitness
        if current > pick:
            return c

def Tournament(parent1,parent2):
    return


# take in paramter of iteration and the current fitness level,
# - if the fitness level increase, control the mu to take the best fitness and slowly reduce it.
# in earlier stage, set the mu to sigma to be higher.
# slowly reduce the sigma in later stage.
def selfAdaptiveGaussianMutationRate():
    mu, sigma = 0, 0.1 # mean and standard deviation
    #s = np.random.normal(mu, sigma, 10)

    #print (abs(mu - np.mean(s)) < 0.01)
    #print (abs(sigma - np.std(s, ddof=1)) < 0.01)

    #num = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (s - mu)**2 / (2 * sigma**2))
    num = np.random.normal(mu,sigma)
    return num


# MISCELLANEOUS TOOL #
def validate_checkConstraint():
    fitness = 0.0

    h = 0.8095680981774316
    w = 0.16138492664005277
    L = 12.49983827668806
    d = 4.66163559389344

    #geneString = "w: {} h: {} L:{} d:{}".format(w,h,L,d)
    #os.system("echo {} >> gene.txt".format(geneString))
    ax = (504000/(h*(math.pow(d,2))))
    Q = 6000*(14+(L/2))
    D = (1/2)*(math.sqrt(math.pow(L,2)+math.pow(w+d,2)))
    J = math.sqrt(2)*w*L*((math.pow(L,2)/6)+(math.pow(w+d,2)/2))
    sx = 65856/((30000)*h*math.pow(D,3))
    b = (Q*D)/J
    a = 6000/(math.sqrt(2)*w*L)
    tx = math.sqrt(math.pow(a,2)+((a*b*L)/D)+math.pow(b,2))
    px = 0.61423*(math.pow(10,6))*((d*math.pow(h,3))/6)*(1-(math.pow(30/48,1/d)/28))


    if w < 0.1:
        print ("fail w")
    elif h > 2.0:
        print ("fail h")
    elif d > 10:
        print ("fail d")
    elif L < 0.1:
        print ("fail L")
    elif (w - h) > 0 :
        print ("fail rule 1")
    elif (sx - 0.25) > 0:
        print ("fail rule 2")
    elif (tx - 13600) > 0:
        print ("fail rule 3")
    elif (ax - 30000) > 0:
        print ("fail rule 4")
    elif ((0.10471*math.pow(w,2)) + (0.04811*h*d*(14+L)) - 5) > 0:
        print ("fail rule 5")
    elif (0.125 - w) > 0:
        print ("fail rule 6")
    elif (6000 - px) > 0:
        print ("fail rule 7")

    fitness = (1.10471*(math.pow(w,2))*L) + (0.04811*d*h*(14.0+L))
    print (fitness)
    return fitness



# # # # # # # # # # # # # # # #
# Run the main function.      #
# # # # # # # # # # # # # # # #
if __name__ == "__main__":
    main(200,100)
    #validate_checkConstraint()
    #fuzzy_system(250,0.87)
