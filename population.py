from individual import Individual
import math

class Population:

    # generate population by the popSize
    def __init__(self,popSize,init):
        self.popSize = popSize
        self.mean = [0.0, 0.0, 0.0, 0.0]
        self.variance = 0.0
        self.stddev = 0.0
        self.pop = []
        if init:
            for _ in range(popSize):
                self.ind = Individual()
                self.insertPopulation(self.ind)

    def __del__(self):
        self.mean = [0.0, 0.0, 0.0, 0.0]
        self.variance = 0.0
        self.stddev = 0.0
        self.pop = []

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
            if not self.getIndividual(_).violation:
                if (fittest.getFitness() > self.getIndividual(_).getFitness()):
                    fittest = self.getIndividual(_)
        
        return fittest;

    def getParticularIndividualFitness(self,index):
        if index <= self.popSize:
            target = self.getIndividual(index)
        return target.getFitness()

    def getParent(self):
        index = random.randint(0,(self.popSize-1))
        return self.getIndividual(index)

    def getMean(self,geneIndex):
        mean = 0.0
        for _ in range(self.popSize):
            mean += self.getIndividual(_).getIndividualGene(geneIndex)
        return mean/self.popSize

    def getVariance(self,geneIndex):
        mean = self.getMean(geneIndex)
        total = 0.0

        for _ in range(self.popSize):
            total += (math.pow(((self.getIndividual(_).getIndividualGene(geneIndex) - mean))/self.popSize,2))

        return total/self.popSize

    def getStandardDeviation(self,geneIndex):
        return math.sqrt(self.getVariance(geneIndex))
