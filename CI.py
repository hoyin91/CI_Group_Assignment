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
        #fitness = (1.10471*target.getLength()*2*target.getDepth()) + ((0.04811*target.getThickness()*target.getWidth()*(14.0+target.getDepth())))
        return target.getFitness()

    def getParent(self):
        index = random.randint(0,(self.popSize-1))
        return self.getIndividual(index)



class Individual:

    # Init gene with random value, each individual has 4 genes
    def __init__(self):
        # init constraint of each parameter
        self.MAXWIDTH = 2.0
        self.MINTHICKNESS = 10.0
        self.MINLENGTH = 0.1
        self.MINDEPTH = 0.1
        self.violation = False # Flag to indicate violation of constraint

        #assign to random.random() for random float (0.0 - 1.0)
        self.width = random.uniform(0.1,self.MAXWIDTH)
        self.length = random.uniform(self.MINLENGTH,2.0)
        self.depth = random.uniform(self.MINDEPTH,5.0)
        self.thickness = random.uniform(self.MINTHICKNESS,100.0)
        self.ind = [self.width, self.length, self.depth, self.thickness]

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
        self.thickness = valueArray[3]
        self.ind = [self.width, self.length, self.depth, self.thickness]

    def setParticularGene(self,index,value):
        if index == 0:
            self.width = value
        elif index == 1:
            self.length = value
        elif index == 2:
            self.depth = value
        elif index == 3:
            self.thickness = value

        self.ind = [self.width, self.length, self.depth, self.thickness]

    def getWidth(self):
        if self.width >= self.MAXWIDTH:
            self.violation = True
            print ("violation Wifdth")
        return self.width

    def getLength(self):
        if self.length <= self.MINLENGTH:
            self.violation = True
            print ("violation length")
        return self.length

    def getThickness(self):
        if self.thickness <= self.MINTHICKNESS:
            self.violation = True
            print ("violation thick")
        return self.thickness

    def getDepth(self):
        if self.depth <= self.MINDEPTH:
            self.violation = True
            print ("violation depth")
        return self.depth

    def getFitness(self):
        self.checkConstraint()
        # if any parameter violate, return 0.0 directly
        if self.violation:
            # reset the violation flag
            self.violation = False
            return 0.0
        else:
            print ("No Failure")
            fitness = (1.10471*self.getLength()*2*self.getDepth()) + ((0.04811*self.getThickness()*self.getWidth()*(14.0+self.getDepth())))
            os.system("echo {} >> testing.txt".format(fitness))
            return fitness

    def checkConstraint(self):
        H=self.getWidth()
        W=self.getLength()
        L=self.getDepth()
        D=self.getThickness()
        print (W,H,L,D)
        ax=(504000/(H*D**2))
        q=6000*(14+(L/2))
        d=(1/2)*(math.sqrt((L**2)+(W+D)**2))
        j=math.sqrt(2)*W*L*(((L**2)/2)+(((W+D)**2)/2))
        sx=(65856/((30000)*H*(D**3)))
        b=(q*D)/j
        a=6000/(math.sqrt(2)*W*L)
        tx= math.sqrt((a**2)+((a*b*L)/D)+(b**2))
        px=0.61423*((10**6)*D*(H**3)/6)*(1-((30/48)**(1/D)/28))


        if W - H >= 0 :
            self.violation=True
            print ("rule 1")
            os.system("echo rule1 >> testing.txt")
        elif sx - 0.25 >=0:
            self.violation=True
            print ("rule 2")
        elif tx - 13600>=0:
            self.violation=True
            print ("rule 3")
        elif ax - 30000 >= 0:
            print ("rule 4")
            self.violation = True
        elif (0.10471*(W**2)) + (0.04811*H*D*(14+L)) - 5 >= 0:
            self.violation = True
            print ("rule 5")
            os.system("echo rule5 >> testing.txt")
        elif 0.125 - W >= 0:
            self.violation = True
            print ("rule 6")
        elif 6000 - px >= 0:
            self.violation = True
            print ("rule 7")
        else:
            print ("no failure")


def simpleArithmeticCrossover(parent1,parent2):
    child1 = Individual()
    child2 = Individual()

    genePosition=random.randint(0,child1.getGeneSize()-1) # take in size of gene from variable
    for x in range(child1.getGeneSize()):
        if x >= genePosition:
            geneValue1 = (recombinationVar*parent2.getIndividualGene(x)+(1-recombinationVar)*parent1.getIndividualGene(x))
            geneValue2 = (recombinationVar*parent1.getIndividualGene(x)+(1-recombinationVar)*parent2.getIndividualGene(x))
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

    # print (child.getIndividualGeneArray())
    for _ in range(child.getGeneSize()):
        MutationRate = random.random()
        if (MutationRate > 0.5): # perform mutation if and only if the mutation rate is higher than 0.5
            #print ("MR: {} Gene @ {}: to geneVal: {}".format(MutationRate,_,child.getIndividualGene(_)))
            # RandomgeneValue = random.random() * 2

            child.setParticularGene(_, RandomgeneValue)

    # print (child.getIndividualGeneArray())
    # return mutated child
    return child

def main():
    popSize = 30
    pop = Population(popSize,1)
    for y in range(100):
        newPop = Population(popSize,0)
        for x in range(int(popSize/2)):
            parent1 = pop.getParent()
            parent2 = pop.getParent()
            child1 = Individual()
            child2 = Individual()
            child1,child2 = simpleArithmeticCrossover(parent1,parent2)
            #Mutation(child1)
            #Mutation(child2)
            newPop.insertPopulation(child1)
            newPop.insertPopulation(child2)
            print(newPop.getParticularIndividualFitness(x))
        else:
            # replace the entire population with newly generated children
            pop = newPop


main()
#abc = Population(2,1)
#Mutation(abc.getParent())

