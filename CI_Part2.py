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
        self.mean = [0.0, 0.0, 0.0]
        self.stdev = [0.0, 0.0, 0.0]
        self.variance = [0.0, 0.0, 0.0]

        if init:
            for _ in range(popSize):
                self.ind = Individual()
                self.insertPopulation(self.ind)

    # destructor to clean up those value when we reassign those param
    def __del__(self):
        self.mean = [0.0, 0.0, 0.0]
        self.stdev = [0.0, 0.0, 0.0]
        self.variance = [0.0, 0.0, 0.0]

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


    def getPopulationMean(self,geneIndex):

        if not self.mean[geneIndex]:
            for _ in range(self.popSize):
                self.mean[geneIndex] += self.getIndividual(_).getIndividualGene(geneIndex)
            else:
                self.mean[geneIndex] = self.mean[geneIndex]/(self.popSize)

        return self.mean[geneIndex]

    def getPopulationVariance(self,geneIndex):
        mean = self.getPopulationMean(geneIndex)
        total = 0.0

        if not self.variance[geneIndex]:
            for _ in range(self.popSize):
                total += math.pow((self.getIndividual(_).getIndividualGene(geneIndex) - mean),2)
            else:
                self.variance[geneIndex] = total/(self.popSize-1)

        return self.variance[geneIndex]

    def getPopulationStdDev(self,geneIndex):
        array = []
        if not self.stdev[geneIndex]:
            for _ in range(self.popSize):
                self.stdev[geneIndex] = math.sqrt(self.getPopulationVariance(geneIndex))

        return self.stdev[geneIndex]

    def getPopulationParameterStdDev(self):
        try:
            ind = Individual()
            for _ in range(ind.getGeneSize()):
                self.getPopulationStdDev(_)

            #print (self.stdev)
            return self.stdev
        except:
            return 0.0001

class Individual:

    # Init gene with random value, each individual has 4 genes
    def __init__(self):
        # init constraint of each parameter
        self.MINWIDTH = 0.05
        self.MAXWIDTH = 2.0

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

        self.checkConstraint()
        while self.violation:
            self.selfGenerating()
            self.checkConstraint()

    def selfGenerating(self):
        self.width = random.uniform(self.MINWIDTH, self.MAXWIDTH)
        self.length = random.uniform(self.MINLENGTH, self.MAXLENGTH)
        self.depth = random.uniform(self.MINDEPTH, self.MAXLENGTH)
        self.ind = [self.width, self.length, self.depth]
        return

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
        if (self.width > self.MAXWIDTH) or (self.width < self.MINWIDTH):
            self.violation = True
        return self.width

    def getLength(self):
        if (self.length < self.MINLENGTH) or (self.length > self.MAXLENGTH):
            self.violation = True
        return self.length

    def getDepth(self):
        if (self.depth < self.MINDEPTH) or (self.depth > self.MAXDEPTH):
            self.violation = True
        return self.depth

    def getFitness(self):
        fitness = 9999
        self.checkConstraint()

        # if any parameter violate, return 9999 directly
        if not self.violation:
            self.fitness = (self.getLength() + 2) * math.pow(self.getWidth(),2) * self.getDepth()

        
        return self.fitness

    def checkConstraint(self):
        self.violation = False
        w=self.getWidth()
        L=self.getLength()
        d=self.getDepth()

        g1 = 1 - ((math.pow(d,3) * L) / (71785*math.pow(w,4))) 
        g2 = 1 - ((140.45 * w) / (math.pow(d,2)*L))
        g3 = ((w*d)/1.5) - 1
        #g4 = ((d*((4*d) - w))/(math.pow(w,3)*((12566*d) - w))) + (1/(5108*math.pow(w,2))) - 1
        g4 = (((4*math.pow(d,2))-(w*d))/((12566*math.pow(w,3)*d)-(12566 * math.pow(w,4)))) + (1/(5108*math.pow(w,2))) - 1

        if g1 > 0:
            self.violation = True
        elif g2 > 0:
            self.violation = True
        elif g3 > 0:
            self.violation = True
        elif g4 > 0:
            self.violation = True


def simpleArithmeticCrossover(parent1,parent2):
    child1 = parent1
    child2 = parent2

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
        mu, sigma = 0, 0.5
    elif iteration > 1500*0.2:
        mu, sigma = 0, 0.1

    for _ in range(child.getGeneSize()):
        if (ProbOfMutation > 0.05):
            #num = random.uniform(0,1)
            RandomgeneValue = child.getIndividualGene(_) + num
            #print ("MR: {} Gene @ {}: to geneVal: {}".format(child.getIndividualGene(_),_,RandomgeneValue))
            child.setParticularGene(_, RandomgeneValue)

    return child

# Main function at here!
def main(generation_count,pop_size):
    popSize = pop_size
    pop = Population(popSize,1)
    for y in range(generation_count):
        newPop = Population(popSize,0)
        successPop = Population(0,0)
        success = 0.0
        array = []
        successList = []
        newlist = []
        #print (pop.getFittest().getIndividualGeneArray())
        print ("Iteration: {} Fitness: {} Array: {}".format(y, (pop.getFittest().getFitness()), pop.getFittest().getIndividualGeneArray()))
        for x in range(int(popSize/2)):
            newlist = []
            array = []
            successList = []
            #parent1 = FPS(pop.getPopulation())
            #parent2 = FPS(pop.getPopulation())
            parent1 = pop.getParent()
            parent2 = pop.getParent()
            child1,child2 = simpleArithmeticCrossover(parent1,parent2)

            if (y > 0) and (x > 0):
                child1 = Mutation2(child1,y,success/x,successPop)
                child2 = Mutation2(child2,y,success/x,successPop)
            else:
                child1 = parent1
                child2 = parent2

            if (child1.getFitness() < parent1.getFitness()):
                #print (child1.getFitness(), parent1.getFitness())
                #print (child1.getFitness(), child1.getIndividualGeneArray(), parent1.getFitness(), parent1.getIndividualGeneArray())
                success += 1

            #print (child2.getFitness(), child2.getIndividualGeneArray(), parent2.getFitness(), parent2.getIndividualGeneArray())

            if (child2.getFitness() < parent2.getFitness()):
                #print (child2.getFitness(), parent2.getFitness())
                #print (child2.getFitness(), child2.getIndividualGeneArray(), parent2.getFitness(), parent2.getIndividualGeneArray())
                success += 1

            array.append(parent1)
            array.append(parent2)
            array.append(child1)
            array.append(child2)
            newlist = sorted(array, key=lambda Individual: Individual.fitness, reverse=False)
            for _ in newlist:
                if y < 2:
                    print (_.getIndividualGeneArray(), _.getFitness())
                    pass
                if _.getFitness() < 100:
                    successList.append(_)
            else:
                if y<2:
                    print ("new set")

            #print (newlist[0].fitness, newlist[1].fitness, newlist[2].fitness, newlist[3].fitness)
            newPop.insertPopulation(newlist[0])
            newPop.insertPopulation(newlist[1])
            #os.system("echo \"P1:{} P2:{} C1:{} C2:{}\" >> testing.txt".format(fitness1, fitness2, fitness3, fitness4))
        else:
            newlist = []
            # replace the entire population with newly generated children
            pop = newPop
            #pop.insertPopulation(newPop.getFittest())
            print(pop.getPopulationParameterStdDev()) #Update the mean

            newsuccessPop = Population(len(successList),0)
            successPop = newsuccessPop
            for _ in successList:
                successPop.insertPopulation(_)
                #print (_.getIndividualGeneArray())
            successPop.getPopulationParameterStdDev()


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

        #num = random.gauss(mu, sigma) * sigma
        num = (random.uniform(0,1)) * np.random.normal(mu, sigma)
        RandomgeneValue = child.getIndividualGene(_) + num
        child.setParticularGene(_, RandomgeneValue)
        #print ("Gene {}: {} After: {}".format(_,num,RandomgeneValue))

    return child

def debug_check():
    valueArray = [0.051653711770636,11.338963731041684,0.355867916029741]
    dut = Individual()
    dut.setIndividualGene(valueArray)
    print (dut.getIndividualGeneArray())
    print (dut.getFitness())

main(30,100)
#debug_check()
