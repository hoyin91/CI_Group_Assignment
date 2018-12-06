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

    #error
    def getFitness(self,index):
    	if index <= self.popSize:
    		target = self.getIndividual(index)
    	#fitness = (1.10471 * target.length * 2 * target.depth)+(0.04811 * target.thickness * target.width *(14.0+target.depth))
    	return target

class Individual:

    # Init gene with random value, each individual has 4 genes
    def __init__(self):
        self.width = random.uniform(0.1,5) #assign to random.random() for random float (0.0 - 1.0)
        self.length = random.uniform(0.01,10)
        self.depth = random.uniform(0.1,2)
        self.thickness = random.uniform(0.01,2)
        self.ind = [self.width, self.length, self.depth, self.thickness]

    # return individual array
    def getIndividualGene(self,index=99):
        if index == 99:
            return self.ind
        else:
            return self.ind[index]

    # set Individual gene value
    def setIndividualGene(self, valueArray):
        self.width = valueArray[0]
        self.length = valueArray[1]
        self.depth = valueArray[2]
        self.thickness = valueArray[3]
        self.ind = [self.width, self.length, self.depth, self.thickness]    



abc = Population(30) #init population with size of 10
print ("Init population")
print (abc.getPopulation())
abc.setPopulationGene(1,[1.2,1.3,1.5,1.7]) #set the particular ind with the gene value
print ("Population fitness after changing gene value")
print (abc.getPopulation()) #print population index
print (abc.getIndividual(1))
print (abc.getIndividual(100))
print (abc.getFitness(9))