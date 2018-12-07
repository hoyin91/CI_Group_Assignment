import random

recombinationVar = 0.7
popSize = 30

class Population:

    # generate population by the popSize
    def __init__(self, popSize,init):
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
        self.MAXWIDTH = 1.5
        self.MAXTHICKNESS = 10
        self.MAXLENGTH = 2
        self.MAXDEPTH = 2
        self.violation = False # Flag to indicate violation of constraint

        #assign to random.random() for random float (0.0 - 1.0)
        self.width = random.uniform(0.1,self.MAXWIDTH)
        self.length = random.uniform(0.01,self.MAXLENGTH)
        self.depth = random.uniform(0.1,self.MAXDEPTH)
        self.thickness = random.uniform(0.01,self.MAXTHICKNESS)
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
        if self.width > self.MAXWIDTH:
            self.violation = True
        return self.width

    def getLength(self):
        if self.length > self.MAXLENGTH:
            self.violation = True
        return self.length

    def getThickness(self):
        if self.thickness > self.MAXTHICKNESS:
            self.violation = True
        return self.thickness

    def getDepth(self):
        if self.depth > self.MAXDEPTH:
            self.violation = True
        return self.depth

    def getFitness(self):

        fitness = (1.10471*self.getLength()*2*self.getDepth()) + ((0.04811*self.getThickness()*self.getWidth()*(14.0+self.getDepth())))

        # if any parameter violate, return 0.0 directly
        if self.violation:
            # reset the violation flag
            self.violation = False
            return 0.0
        else:
            return fitness



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

    # print (child.getIndividualGeneArray())
    for _ in range(child.getGeneSize()):
        MutationRate = random.random()
        if (MutationRate > 0.5): # do mutation if and only if the mutation rate is higher than 0.5
            #print ("MR: {} Gene @ {}: to geneVal: {}".format(MutationRate,_,child.getIndividualGene(_)))
            RandomgeneValue = random.random() * 2
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
            Mutation(child1)
            Mutation(child2)
            newPop.insertPopulation(child1)
            newPop.insertPopulation(child2)
        else:
            # replace the entire population with newly generated children
            pop = newPop

main()
    
