import random

class Population:

    # generate population by the popSize
    def __init__(self, popSize):
        self.popSize = popSize
        self.pop = []
        for _ in range(popSize):
            self.ind = Individual()
            self.generatePopulation(self.ind.getIndividualGene())

    # generate population (array)
    def generatePopulation(self,ind):
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

    # not done yet
    def getFittest(self):
        # Loop through individuals to find fittest
        fittest = self.pop[0]
        print (fittest)
        for _ in range(self.popSize):
            if (fittest.getFitness() <= self.getIndividual(_).getFitness()):
                fittest = self.getIndividual(_)
        
        return fittest;

    # not done yet
    def getFitness(self):
        return 1.0

class Individual:

    # Init gene with random value, each individual has 4 genes
    def __init__(self):
        self.gene1 = 0.0 #assign to random.random() for random float (0.0 - 1.0)
        self.gene2 = 0.0
        self.gene3 = 0.0
        self.gene4 = 0.0
        self.ind = [self.gene1, self.gene2, self.gene3, self.gene4]

    # return individual array
    def getIndividualGene(self,index=99):
        if index == 99:
            return self.ind
        else:
            return self.ind[index]

    # set Individual gene value
    def setIndividualGene(self, valueArray):
        self.gene1 = valueArray[0]
        self.gene2 = valueArray[1]
        self.gene3 = valueArray[2]
        self.gene4 = valueArray[3]
        self.ind = [self.gene1, self.gene2, self.gene3, self.gene4]



abc = Population(10) #init population with size of 10
print ("Init population")
print (abc.getPopulation())
abc.setPopulationGene(1,[1.2,1.3,1.5,1.7]) #set the particular ind with the gene value
print ("Population fitness after changing gene value")
print (abc.getPopulation()) #print population index
print (abc.getIndividual(1))
print (abc.getIndividual(100))
