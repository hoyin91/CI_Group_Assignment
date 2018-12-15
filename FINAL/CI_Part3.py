import random
import numpy as np
import math
import os
import skfuzzy as fuzz
import copy

recombinationVar = 0.7

class Population:

    # generate population by the popSize
    def __init__(self,popSize,init):
        self.popSize = popSize
        self.pop = []
        self.mean = [0.0, 0.0, 0.0, 0.0]
        self.stdev = [0.0, 0.0, 0.0, 0.0]
        self.variance = [0.0, 0.0, 0.0, 0.0]

        if init:
            for _ in range(popSize):
                self.ind = Individual()
                self.insertPopulation(self.ind)

    # destructor to clean up those value when we reassign those param
    def __del__(self):
        self.mean = [0.0, 0.0, 0.0, 0.0]
        self.stdev = [0.0, 0.0, 0.0, 0.0]
        self.variance = [0.0, 0.0, 0.0, 0.0]

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
        if index < self.popSize:
            return self.pop[index]

    def getFittest(self):
        # Loop through individuals to find fittest
        fittestInd = self.getIndividual(0)
        for _ in range(self.popSize):
            if (fittestInd.getFitness() < self.getIndividual(_).getFitness()):
                fittestInd = self.getIndividual(_)
        
        return fittestInd

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
        if not self.stdev[geneIndex]:
            for _ in range(self.popSize):
                self.stdev[geneIndex] = math.sqrt(self.getPopulationVariance(geneIndex))

        return self.stdev[geneIndex]

    def getPopulationParameterStdDev(self):
        try:
            ind = Individual()
            for _ in range(ind.getGeneSize()):
                self.getPopulationStdDev(_)
            return self.stdev
        except:
            return 0.01

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
        self.thicknessHead = random.uniform(0.01, self.MAXTHICKNESSHEAD)
        self.thickness = random.uniform(self.MINTHICKNESS, 10)
        self.innerRadius = random.uniform(self.MININNERRADIUS,50)
        self.length = random.uniform(0.01,self.MAXLENGTH)
        self.ind = [self.thicknessHead, self.thickness, self.innerRadius, self.length]


        # check if newly generated function is within constraint or not
        # regenerate until it meets the constraint requirement.
        self.checkConstraint()
        while self.violation:
            self.selfGenerating()
            self.checkConstraint()

    def selfGenerating(self):
        #assign to random.random() for random float (0.0 - 1.0)
        self.thicknessHead = random.uniform(0.01, self.MAXTHICKNESSHEAD)
        self.thickness = random.uniform(self.MINTHICKNESS, 10)
        self.innerRadius = random.uniform(self.MININNERRADIUS,50)
        self.length = random.uniform(0.01,self.MAXLENGTH)
        self.ind = [self.thicknessHead, self.thickness, self.innerRadius, self.length]
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
        for k,v in enumerate(valueArray):
            self.setParticularGene(k,v)
        self.ind = [self.thicknessHead, self.thickness, self.innerRadius, self.length]

    def setParticularGene(self,index,value):
        if index == 0:
            self.thicknessHead = value
        elif index == 1:
            self.thickness = value
        elif index == 2:
            self.innerRadius = value
        elif index == 3:
            self.length = value

        self.ind = [self.thicknessHead, self.thickness, self.innerRadius, self.length]

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
        self.fitness = 0.0
        self.checkConstraint()

        # if any parameter violate, return 9999 directly
        if not self.violation:
            a=(0.6224*self.getThickness()*self.getInnerRadius()*self.getLength())
            b=(1.7781*self.getThicknessHead()*self.getInnerRadius()*self.getThicknessHead())
            c=(3.1661*math.pow(self.getThickness(),2)*self.getLength())
            d=(19.84*math.pow(self.getThickness(),2)*self.getInnerRadius())
            self.fitness = (a + b + c + d)

        return self.fitness

    def checkConstraint(self):
        self.violation = False
        PI = 3.141592557
        ts=self.getThickness()
        th=self.getThicknessHead()
        L=self.getLength()
        R=self.getInnerRadius()

        if (-ts + (0.0193*R)) > 0 :
            self.violation=True
            #print ("fail rule 1")
        elif (-th + (0.00954*R)) > 0:
            self.violation=True
            #print ("fail rule 2")
        elif ((-PI*math.pow(R,2)*L)-(((4*PI)/3)*math.pow(R,3))+1296000) > 0:
            self.violation=True
            #print ("fail rule 3")
        elif (L - 240) > 0:
            self.violation = True
            #print ("fail rule 4")

def simpleArithmeticCrossover(parent1,parent2):
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

    genePosition=random.randint(0,parent1.getGeneSize()-1) # take in size of gene from variable
    for x in range(parent1.getGeneSize()):
        if x >= genePosition:
            geneValue1 = ((recombinationVar*parent2.getIndividualGene(x))+((1-recombinationVar)*parent1.getIndividualGene(x)))
            geneValue2 = ((recombinationVar*parent1.getIndividualGene(x))+((1-recombinationVar)*parent2.getIndividualGene(x)))
            child1.setParticularGene(x,geneValue1)
            child2.setParticularGene(x,geneValue2)
        else:
            child1.setParticularGene(x,parent1.getIndividualGene(x))
            child2.setParticularGene(x,parent2.getIndividualGene(x))

    # return both children
    return child1,child2

# Mutation algorithm
def Mutation(parent, iteration, success_rate, population):
    child = copy.deepcopy(parent)
    c = random.uniform(0.87,1.0)

    for _ in range(child.getGeneSize()):
        sigma = copy.deepcopy(population.getPopulationStdDev(_))
        mu = copy.deepcopy(population.mean[_])
        if iteration % 50 == 0:
            if success_rate > 0.2:
                sigma = sigma/c
            elif success_rate < 0.2:
                sigma = sigma * c
            elif success_rate == 0.2:
                sigma = sigma
        else:
            sigma = sigma

        num = random.uniform(0,1) * random.gauss(mu, sigma) * sigma
        RandomgeneValue = child.getIndividualGene(_) - num
        child.setParticularGene(_, RandomgeneValue)

    return child

# fuzzy function
def fuzzy_system(generation_val,convergence_val):
    x_generation = np.arange(0, 1500, 50)
    x_convergence = np.arange(0, 1, 0.1)
    x_recombinationRate  = np.arange(0, 0.5, 0.1)

    # Generate fuzzy membership functions
    generation_lo = fuzz.trapmf(x_generation, [0, 0, 300,500])
    generation_md = fuzz.trimf(x_generation, [500, 750, 1000])
    generation_hi = fuzz.trapmf(x_generation, [1000, 1200, 1500,1500])
    convergence_lo = fuzz.trapmf(x_convergence, [0, 0, 0.2,0.3])
    convergence_md = fuzz.trapmf(x_convergence, [0.25, 0.4,0.6, 0.75])
    convergence_hi = fuzz.trapmf(x_convergence, [0.7, 0.8, 1,1])
    recom_lo = fuzz.trapmf(x_recombinationRate, [0, 0, 0.15,0.2])
    recom_md = fuzz.trapmf(x_recombinationRate, [0.15, 0.2, 0.3, 0.35])
    recom_hi = fuzz.trapmf(x_recombinationRate, [0.3, 0.4, 0.5,0.5])

    generation_level_lo = fuzz.interp_membership(x_generation, generation_lo, generation_val)
    generation_level_md = fuzz.interp_membership(x_generation, generation_md, generation_val)
    generation_level_hi = fuzz.interp_membership(x_generation, generation_hi, generation_val)

    convergence_level_lo = fuzz.interp_membership(x_convergence, convergence_lo, convergence_val)
    convergence_level_md = fuzz.interp_membership(x_convergence, convergence_md, convergence_val)
    convergence_level_hi = fuzz.interp_membership(x_convergence, convergence_hi, convergence_val)

    active_rule1 = np.fmax(generation_level_hi, convergence_level_hi)
    rate_activation_lo = np.fmin(active_rule1, recom_lo)

    active_rule2 = np.fmax(generation_level_md,convergence_level_md)
    rate_activation_md = np.fmin(active_rule2,recom_md)

    active_rule3 = np.fmin(generation_level_lo,convergence_level_md)
    active_rule4 = np.fmin(active_rule3, np.fmin(generation_level_lo, convergence_level_lo))
    rate_activation_hi = np.fmin(active_rule4, recom_hi)

    aggregated = np.fmax(rate_activation_lo, np.fmax(rate_activation_md, rate_activation_hi))
    recom_rate = fuzz.defuzz(x_recombinationRate, aggregated, 'centroid')

    #print("recombination rate = "+str(recom_rate))
    return recom_rate

def debug_check():
    valueArray = [0.812500000000000,0.437500000000000,42.098445593492706,176.6365958720004]
    #valueArray = [4.751114909557465, 9.861871448799207, 47.326035144970824, 193.25824076155143]
    dut = Individual()
    dut.setIndividualGene(valueArray)
    print (dut.getIndividualGeneArray())
    print (dut.getFitness())

# Main function at here!
def main(generation_count,pop_size):
    popSize = pop_size
    pop = Population(popSize,1)
    for y in range(generation_count):
        newPop = Population(popSize,0)
        successPop = Population(0,0)
        success = 0.0
        fittestoftheloop = copy.deepcopy(pop.getFittest())
        newPop.insertPopulation(fittestoftheloop)
        print ("Iteration: {} Fitness: {} Array: {} stddev: {}".format(y, fittestoftheloop.getFitness(), fittestoftheloop.getIndividualGeneArray(), pop.getPopulationParameterStdDev()))
        os.system("echo {} >> result_2.txt".format(fittestoftheloop.getFitness()))
        for x in range(int(popSize/2)):
            parent1 = pop.getParent()
            parent2 = pop.getParent()

            child1,child2 = simpleArithmeticCrossover(parent1,parent2)

            # Mutate the child based on the successrate and std dev
            if (y > 0) and (x > 0):
                child1 = Mutation(child1,y,success/x,successPop)
                child2 = Mutation(child2,y,success/x,successPop)
            else:
                child1 = parent1
                child2 = parent2

            # check if child is fitter than its parent or not
            # if yes, increase the counter for the prob success mutation
            if (child1.getFitness() < parent1.getFitness()):
                newPop.insertPopulation(child1)
                success += 1
            else:
                newPop.insertPopulation(parent1)

            if (child2.getFitness() < parent2.getFitness()):
                newPop.insertPopulation(child2)
                success += 1
            else:
                newPop.insertPopulation(parent2)
        else:
            # replace the entire population with newly generated children'
            pop = copy.deepcopy(newPop)
            pop.getPopulationParameterStdDev() #Update the mean

#main(10,100)
debug_check()
