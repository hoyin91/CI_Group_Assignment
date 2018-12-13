import random
import numpy as np
import math
import os

recombinationVar = 0.7
popSize = 30

class Population:

    # generate population by the popSize
    def __init__(self,popSize,init):
        self.popSize = popSize
        self.pop = []
        if init:
            for _ in range(popSize):
                self.ind = Individual()
                self.insertPopulation(self.ind)

    # generate population (array)
    def insertPopulation(self,ind):
        self.pop.append(ind)
        
    # return population (Array of float)
    def getPopulation(self):
        return self.pop

    # set the gene of particular individual from the population
    def setPopulationGene(self,indIndex, arrayGene):
        self.pop[indIndex] = self.ind.setIndividualGene(arrayGene)
        self.pop[indIndex] = self.ind.getIndividualGene()

    def getIndividual(self,index):
        if index <= self.popSize:
            return self.pop[index]

    def getFittest(self):
        # Loop through individuals to find fittest
        fittest = self.getIndividual(0)
        for _ in range(self.popSize):
            if (fittest.getFitness() <= self.getIndividual(_).getFitness()):
                fittest = self.getIndividual(_)
        
        return fittest;

    def getParticularIndividualFitness(self,index):
        if index <= self.popSize:
            target = self.getIndividual(index)
        return target.getFitness()

    def getParent(self):
        index = random.randint(0,(self.popSize-1))
        return self.getIndividual(index)


class Individual:

    # Init gene with random value, each individual has 4 genes
    def __init__(self):
        # init constraint of each parameter
        self.MAXWIDTH = 2.0
        self.MINWIDTH = 0.05

        self.MINLENGTH = 2.0
        self.MAXLENGTH = 15.0

        self.MINDEPTH = 0.25
        self.MAXDEPTH = 1.3

        self.violation = False # Flag to indicate violation of constraint
        self.fitness = 0.0

        #assign to random.random() for random float (0.0 - 1.0)
        self.width = random.uniform(self.MINWIDTH, self.MAXWIDTH)
        self.length = random.uniform(self.MINLENGTH,self.MAXLENGTH)
        self.depth = random.uniform(self.MINDEPTH,self.MAXLENGTH)
        self.ind = [self.width, self.length, self.depth]

    # get the gene array size
    def getGeneSize(self):
        return len(self.ind)

    # get the individual array directly
    def getIndividualGeneArray(self):
        return self.ind

    # return individual array
    def getIndividualGene(self,index):
        return self.ind[index]

    # set Individual gene value
    def setIndividualGene(self, valueArray):
        self.width = valueArray[0]
        self.length = valueArray[1]
        self.depth = valueArray[2]
        self.ind = [self.width, self.length, self.depth]

    def setParticularGene(self,index,value):
        if index == 0:
            self.width = value
        elif index == 1:
            self.length = value
        elif index == 2:
            self.depth = value

        self.ind = [self.width, self.length, self.depth]

    def getWidth(self):
        if self.width > self.MAXWIDTH or self.width < self.MINWIDTH:
            self.violation = True
            self.width = random.uniform(self.MINWIDTH, self.MAXWIDTH)
        return self.width

    def getLength(self):
        if self.length < self.MINLENGTH or self.length > self.MAXLENGTH:
            self.violation = True
            self.width = random.uniform(self.MINLEGNTH, self.MAXWIDTH)
        return self.length

    def getDepth(self):
        if self.depth < self.MINDEPTH or self.depth > self.MAXDEPTH:
            self.violation = True
            self.depth = random.uniform(self.MINDEPTH, self.MAXDEPTH)
        return self.depth

    def getFitness(self):
        fitness = 0.0
        self.checkConstraint()

        # if any parameter violate, return 0.0 directly
        if self.violation:
            # reset the violation flag
            return 0.001
        else:
            fitness = (self.getLength()/2) * math.pow(self.getWidth(),2) * self.getDepth() 
            return fitness

    def checkConstraint(self):
        self.violation = False
        w=self.getWidth()
        L=self.getLength()
        d=self.getDepth()
        print (w,L,d)
        g1 = 1 - ((math.pow(d,3) * L) / (71785*math.pow(w,4)))
        print (g1)
        g2 = 1 - ((149.45 * w) / (math.pow(d,2)*L))
        g3 = ((2*(w*d))/3) - 1
        g4 = (d*((4*d) - w))/(math.pow(w,4)*((12566*d) - w)) + (1/(5108*math.pow(w,2))) - 1

        if g1 > 0:
            print ("fail rule1")
            self.violation = True
        elif g2 > 0:
            print ("fail rule2")
            self.violation = True
        elif g3 > 0:
            print ("fail rule3")
            self.violation = True
        elif g4 > 0:
            print ("fail rule4")
            self.violation = True

        if self.violation:
            pass
        else:
            print ("FIT")


def simpleArithmeticCrossover(parent1,parent2):
    child1 = Individual()
    child2 = Individual()

    genePosition=random.randint(0,parent1.getGeneSize()) # take in size of gene from variable
    for x in range(parent1.getGeneSize()):
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

    # return both children
    return child1,child2

# MUTATION ALGORITHM
def Mutation(parent,iteration):
    # Init child1 as parent to undergo mutation
    child = parent
    ProbOfMutation = random.random()
    
    # init mu and sigma
    mu,sigma = 0,0.1

    if iteration < 1500*0.2:
        mu, sigma = 0, 1
    elif iteration > 1500*0.2:
        mu, sigma = 0, 0.1

    for _ in range(child.getGeneSize()):
        if (ProbOfMutation > 0.05):
            num = random.gauss(mu,sigma)
            RandomgeneValue = child.getIndividualGene(_) + num
            # print ("MR: {} Gene @ {}: to geneVal: {}".format(MutationRate,_,RandomgeneValue))
            child.setParticularGene(_, RandomgeneValue)

    return child

# Main function at here!
def main(generation_count,pop_size):
    popSize = pop_size
    pop = Population(popSize,1)
    for y in range(generation_count):
        newPop = Population(popSize,0)
        newPop.insertPopulation(pop.getFittest())
        print ("Iteration: {} Fitness: {}".format(y, 1/(pop.getFittest().getFitness())))
        for x in range(int(popSize/2)):
            parent1 = FPS(pop.getPopulation())
            parent2 = FPS(pop.getPopulation())
            child1,child2 = simpleArithmeticCrossover(parent1,parent2)
            Mutation(child1,y)
            Mutation(child2,y)

            fitness3 = child1.getFitness()
            fitness4 = child2.getFitness()

            newPop.insertPopulation(child1)
            newPop.insertPopulation(child2)
            #os.system("echo \"P1:{} P2:{} C1:{} C2:{}\" >> testing.txt".format(fitness1, fitness2, fitness3, fitness4))
        else:
            # replace the entire population with newly generated children
            pop = newPop
    else:
        print (pop.getFittest().getFitness())


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

main(1000,200)
