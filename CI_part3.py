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
        self.MAXTHICKNESSHEAD = 0.0625*99
        self.MINTHICKNESS = 0.0625
        self.MININNERRADIUS = 10
        self.MAXLENGTH = 200
        self.violation = False # Flag to indicate violation of constraint

        #assign to random.random() for random float (0.0 - 1.0)

        self.thickness = random.uniform(self.MINTHICKNESS, 6)
        self.thicknessHead = random.uniform(0.1, self.MAXTHICKNESSHEAD)
        self.innerRadius = random.uniform(self.MININNERRADIUS,100)
        self.length = random.uniform(0.1,self.MAXLENGTH)
        self.ind = [self.thicknessHead, self.thickness, self.innerRadius, self.length]
        #print (self.ind)

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
        if self.length < self.MAXLENGTH:
            self.violation = True
        return self.length

    def getFitness(self):
        fitness = 0.0
        self.checkConstraint()

        # if any parameter violate, return 0.0 directly
        if self.violation:
            # reset the violation flag
            return 0.0
        else:
            a=(0.6224*self.getThickness()*self.getInnerRadius()*self.getLength())
            b=(1.7781*self.getThicknessHead()*math.pow(self.getInnerRadius(),2))
            c=(3.1661*math.pow(self.getThickness(),2)*self.getLength())
            d=(19.84*math.pow(self.getThicknessHead(),2)*self.getInnerRadius())
            fitness = a+b+c+d
            geneString = "h: {} w: {} L:{} d:{} Fitness: {}".format(self.thickness,self.thicknessHead,self.innerRadius,self.length,fitness)
            print (geneString)
            return fitness

    def checkConstraint(self):
        self.violation = False
        ts=self.getThickness()
        th=self.getThicknessHead()
        L=self.getLength()
        R=self.getInnerRadius()
        #print (W,H,L,D)
        #geneString = "w: {} h: {} L:{} d:{}".format(w,h,L,d)
        #os.system("echo {} >> gene.txt".format(geneString))

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
        for x in range(int(popSize/2)):
            parent1 = pop.getParent()
            parent2 = pop.getParent()
            child1,child2 = simpleArithmeticCrossover(parent1,parent2)
            Mutation(child1)
            Mutation(child2)
            #fitness1 = parent1.getFitness()
            #fitness2 = parent2.getFitness()
            fitness3 = child1.getFitness()
            fitness4 = child2.getFitness()
            
            newPop.insertPopulation(child1)
            newPop.insertPopulation(child2)
            #os.system("echo \"P1:{} P2:{} C1:{} C2:{}\" >> testing.txt".format(fitness1, fitness2, fitness3, fitness4))
        else:
            # replace the entire population with newly generated children
            pop = newPop


def validate_checkConstraint():
    fitness = 0.0

    L = 1.4313509130700104
    d = 7.25774482387524
    w = 0.5794571665426457
    h = 0.6109559551234784
    #print (W,H,L,D)
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
        print ("fail rule 1")
    elif (tx - 13600) > 0:
        print ("fail rule 1")
    elif (ax - 30000) > 0:
        print ("fail rule 1")
    elif ((0.10471*math.pow(w,2)) + (0.04811*h*d*(14+L)) - 5) > 0:
        print ("fail rule 1")
    elif (0.125 - w) > 0:
        print ("fail rule 1")
    elif (6000 - px) > 0:
        print ("fail rule 1")

    fitness = (1.10471*(math.pow(w,2))*L) + (0.04811*d*h*(14.0+L))
    return fitness

main()
#print (validate_checkConstraint())
