import random
import numpy as np
import math
import os
from individual import Individual


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
        self.MAXTHICKNESSHEAD = 0.0625*99
        self.MINTHICKNESS = 0.0625
        self.MININNERRADIUS = 10
        self.MAXLENGTH = 200
        self.violation = False # Flag to indicate violation of constraint

        #assign to random.random() for random float (0.0 - 1.0)

        self.thickness = random.uniform(self.MINTHICKNESS, 10)
        self.thicknessHead = random.uniform(0.1, self.MAXTHICKNESSHEAD)
        self.innerRadius = random.uniform(self.MININNERRADIUS,20)
        self.length = random.uniform(10,self.MAXLENGTH)
        self.ind = [self.thicknessHead, self.thickness, self.innerRadius, self.length]

        self.checkConstraint()

        #print ("start to stuck")
        #while self.violation:
        #    self.checkConstraint()
        #    self.getFitness()
        #    print ("regenerating")

        #print ("generated")

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
        self.thickness = valueArray[0]
        self.thicknessHead = valueArray[1]
        self.innerRadius = valueArray[2]
        self.length = valueArray[3]
        self.ind = [self.thickness, self.thicknessHead, self.innerRadius, self.length]

    def setParticularGene(self,index,value):
        if index == 0:
            self.thickness = value
        elif index == 1:
            self.thicknessHead = value
        elif index == 2:
            self.innerRadius = value
        elif index == 3:
            self.length = value

        self.ind = [self.thickness, self.thicknessHead, self.innerRadius, self.length]

    def getThickness(self):
        if self.thickness < self.MINTHICKNESS:
            self.violation = True
        return self.thickness

    def getThicknessHead(self):
        if self.thicknessHead > self.MAXTHICKNESSHEAD:
            self.violation = True
        return self.thicknessHead

    def getInnerRadius(self):
        if self.innerRadius < self.MININNERRADIUS:
            self.violation = True
        return self.innerRadius

    def getLength(self):
        if self.length > self.MAXLENGTH:
            self.violation = True
        return self.length

    def getFitness(self):
        fitness = 0.0
        self.checkConstraint()

        # if any parameter violate, return 0.0 directly
        if self.violation:
            # reset the violation flag
            return 0.001
        else:
            a=(0.6224*self.getThickness()*self.getInnerRadius()*self.getLength())
            b=(1.7781*self.getThicknessHead()*math.pow(self.getInnerRadius(),2))
            c=(3.1661*math.pow(self.getThickness(),2)*self.getLength())
            d=(19.84*math.pow(self.getThicknessHead(),2)*self.getInnerRadius())
            fitness = a+b+c+d
            #geneString = "h: {} w: {} L:{} d:{} Fitness: {}".format(self.thickness,self.thicknessHead,self.innerRadius,self.length,fitness)
            #print (geneString)
            return fitness

    def checkConstraint(self):
        self.violation = False
        ts=self.getThickness()
        th=self.getThicknessHead()
        L=self.getLength()
        R=self.getInnerRadius()
        #print (ts,th,L,R)
        geneString = "w: {} h: {} L:{} d:{}".format(ts,th,L,R)
        #os.system("echo {} >> genes_py3.txt".format(geneString))

        if (-ts + (0.0193*R)) > 0 :
            self.violation=True
        elif (-th + (0.0095*R)) > 0:
            self.violation=True
        elif ((-math.pi*math.pow(R,2)*L)-((4*math.pi/3)*math.pow(R,3))+1296000) > 0:
            self.violation=True
        elif (L - 240) > 0:
            self.violation = True

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

    # return both children
    return child1,child2

def Mutation(parent):
    # Init child1 as parent to undergo mutation
    child = parent
    ProbOfMutation = random.random()
    c = random.uniform(0.8,1.0)

    # init mu and sigma
    mu,sigma = 0,0.1


    s = np.random.normal(mu, sigma, 1000)
    #deltasigma = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2)
    num = min(10, max(0, random.gauss(0, 1)))
    # print (child.getIndividualGeneArray())
    for _ in range(child.getGeneSize()):
        RandomgeneValue = child.getIndividualGene(_) + num
        # print ("MR: {} Gene @ {}: to geneVal: {}".format(MutationRate,_,RandomgeneValue))
        child.setParticularGene(_, RandomgeneValue)

    # print (child.getIndividualGeneArray())
    # return mutated child
    return child

def main():
    popSize = 50
    pop = Population(popSize,1)
    for y in range(1000):
        newPop = Population(popSize,0)
        print ("Iteration: {} Fitness: {}".format(y, 1/(pop.getFittest().getFitness())))
        for x in range(int(popSize/2)):
            parent1 = pop.getParent()
            parent2 = pop.getParent()
            child1,child2 = simpleArithmeticCrossover(parent1,parent2)
            Mutation(child1)
            Mutation(child2)
            fitness3 = child1.getFitness()
            fitness4 = child2.getFitness()
            newPop.insertPopulation(child1)
            newPop.insertPopulation(child2)
            #os.system("echo \"P1:{} P2:{} C1:{} C2:{}\" >> testing.txt".format(fitness1, fitness2, fitness3, fitness4))
        else:
            # replace the entire population with newly generated children
            pop = newPop


main()
#print (validate_checkConstraint())
