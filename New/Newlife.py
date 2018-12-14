from population import Population
from individual import Individual
import random
import numpy as np
import math
import os

# Main function at here!
def main(generation_count,popSize):
    pop = Population(popSize,1)
    for y in range(generation_count):
        #os.system("echo Iteration:{} >> testing.txt".format(y))
        newPop = Population(popSize,0)
        success = 0.0
        array = []
        successList = []

        if not successList:
            successPop = Population(2,1)

        #print (pop.getFittest().getIndividualGeneArray())
        print ("Iteration: {} Fitness: {} Array: {}".format(y, (pop.getFittest().getFitness()), pop.getFittest().getIndividualGeneArray()))
        for x in range(1,int(popSize/2)+1):
            parent1 = pop.getParent()
            parent2 = pop.getParent()
            child1,child2 = simpleArithmeticCrossover(parent1,parent2)

            child1 = Mutation2(child1,y,success/x,successPop)
            child2 = Mutation2(child2,y,success/x,successPop)

            if (child1.getFitness() < parent1.getFitness()):
                #print (child1.getFitness(), parent1.getFitness())
                print (child1.getFitness(), child1.getIndividualGeneArray(), parent1.getFitness(), parent1.getIndividualGeneArray())
                success += 1

            if (child2.getFitness() < parent2.getFitness()):
                #print (child2.getFitness(), parent2.getFitness())
                print (child2.getFitness(), child2.getIndividualGeneArray(), parent2.getFitness(), parent2.getIndividualGeneArray())
                success += 1

            array.append(parent1)
            array.append(parent2)
            array.append(child1)
            array.append(child2)
            newlist = sorted(array, key=lambda Individual: Individual.fitness, reverse=False)

            for _ in newlist:
                if _.getFitness() != 9999:
                    successList.append(_)

            newPop.insertPopulation(newlist[0])
            newPop.insertPopulation(newlist[1])
        else:
            # replace the entire population with newly generated children
            pop = newPop
            pop.getPopulationParameterStdDev() #Update the mean

            successPop = Population(len(successList),0)

            for _ in successList:
                successPop.insertPopulation(_)
            successPop.getPopulationParameterStdDev()

            pop.insertPopulation(newPop.getFittest())
            #os.system("echo ADDING_NEW_GEN >> testing.txt")
            #for _ in range(pop.popSize):
            #    #print (pop.getIndividual(_).getIndividualGeneArray())
            #    os.system("echo {} >> testing.txt".format(pop.getIndividual(_).getIndividualGeneArray()))
    else:
        # print out the fitness' gene array
        print ("Iteration: {} Fitness: {} Array: {}".format(y+1, (pop.getFittest().getFitness()), pop.getFittest().getIndividualGeneArray()))

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
            #geneValue1 = (recombinationVar*parent2.getIndividualGene(x)+(1-recombinationVar)*parent1.getIndividualGene(x))
            #geneValue2 = (recombinationVar*parent1.getIndividualGene(x)+(1-recombinationVar)*parent2.getIndividualGene(x))
            geneValue2 = parent1.getIndividualGene(x)
            geneValue1 = parent2.getIndividualGene(x)
            child1.setParticularGene(x,geneValue1)
            child2.setParticularGene(x,geneValue2)
        else:
            child1.setParticularGene(x,parent1.getIndividualGene(x))
            child2.setParticularGene(x,parent2.getIndividualGene(x))

    #print (child1.getIndividualGeneArray(), child1.getFitness())
    #print (child2.getIndividualGeneArray(), child2.getFitness())
    # return both children
    return child1,child2


# MUTATION ALGORITHM
def Mutation(parent,iteration, population):
    # Init child1 as parent to undergo mutation
    child = parent
    ProbOfMutation = random.uniform(0,1)
    
    for _ in range(child.getGeneSize()):
        if (ProbOfMutation > 0.3):
            RandomgeneValue = child.getIndividualGene(_) + (random.gauss(0,0.4)*population.getPopulationStdDev(_))
            child.setParticularGene(_, RandomgeneValue)

    #print (child.getIndividualGeneArray(), child.getFitness())
    # return mutated child
    return child

def Mutation2(parent, iteration, success_rate, population):
    child = parent
    c = random.uniform(0.87,1.0)

    for _ in range(child.getGeneSize()):
        sigma = population.getPopulationStdDev(_)
        mu = population.mean[_]
        if iteration%10 == 0:
            if success_rate > 0.2:
                sigma = sigma/c
            elif success_rate < 0.2:
                sigma = sigma * c
            elif success_rate == 0.2:
                sigma = sigma
        else:
            sigma = sigma

        num = random.gauss(mu, sigma) * sigma
        RandomgeneValue = child.getIndividualGene(_) + num
        child.setParticularGene(_, RandomgeneValue)

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


# MISCELLANEOUS TOOL #
def validate_checkConstraint():
    fitness = 0.0

    h = 0.5290842479592505
    w = 0.16482844280802023
    L = 9.147574876400391
    d = 7.294555353430935

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
    #px = 0.61423*(math.pow(10,6))*((d*math.pow(h,3))/6)*(1-(math.pow(30/48,1/d)/28))
    # print (h, d)
    px = 0.61423*(math.pow(10,6))*((d*math.pow(h,3))/6)*(1- (math.pow(math.exp(1), math.log(30/48)/d)))

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

    fitness = (1.10471*(math.pow(w,2))*L) + (0.04811*d*h*(14.0-L))
    print (fitness)
    return fitness


# # # # # # # # # # # # # # # #
# Run the main function.      #
# # # # # # # # # # # # # # # #
if __name__ == "__main__":
    main(10000,100)
    #validate_checkConstraint()
