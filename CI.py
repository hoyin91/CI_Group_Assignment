import random
import numpy as np
import math
import os
import skfuzzy as fuzz
import numpy.random as npr

def fuzzy_system(generation_val,convergence_val):
    x_generation = np.arange(0, 1500, 50)
    x_convergence = np.arange(0, 1, 0.1)
    x_recombinationRate  = np.arange(0, 0.5, 0.1)

    # Generate fuzzy membership functions
    generation_lo = fuzz.trapmf(x_generation, [0, 0, 300,500])
    generation_md = fuzz.trimf(x_generation, [500, 750, 1000])
    generation_hi = fuzz.trapmf(x_generation, [1000, 1200, 1500,1500])
    convergence_lo = fuzz.trapmf(x_convergence, [0, 0, 0.2,0.3])
    convergence_md = fuzz.trapmf(x_convergence, [0.3, 0.4,0.6, 0.7])
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
    rate_activation_md = np.fmax(active_rule2,recom_md)

    active_rule3 = np.fmin(generation_level_lo,convergence_level_md)
    active_rule4 = np.fmax(active_rule3, np.fmin(generation_level_lo, convergence_level_lo))
    rate_activation_hi = np.fmax(active_rule4, recom_hi)


    aggregated = np.fmax(rate_activation_lo, np.fmax(rate_activation_md, rate_activation_hi))
    recom_rate = fuzz.defuzz(x_recombinationRate, aggregated, 'centroid')

    print("recombination rate = "+str(recom_rate))
    return recom_rate


# Global variable setting
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
        self.MAXTHICKNESS = 10.0
        self.MINLENGTH = 0.1
        self.MINDEPTH = 0.1
        self.violation = False # Flag to indicate violation of constraint

        #assign to random.random() for random float (0.0 - 1.0)
        self.width = random.uniform(0.01, self.MAXWIDTH)
        self.length = random.uniform(self.MINLENGTH,self.width)
        self.depth = random.uniform(self.MINDEPTH,2.0)
        self.thickness = random.uniform(6,self.MAXTHICKNESS)
        self.ind = [self.width, self.length, self.depth, self.thickness]
        self.fitness = 0.0
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

        if self.width < 0:
            self.width = random.uniform(0.1, self.MAXWIDTH)

        return self.width

    def getLength(self):
        if self.length < self.MINLENGTH:
            self.violation = True

        if self.length < 0:
            self.length = random.uniform(self.MINLENGTH,self.width)

        return self.length

    def getThickness(self):
        if self.thickness > self.MAXTHICKNESS:
            self.violation = True

        if self.thickness < 0:
            self.thickness = random.uniform(6,self.MAXTHICKNESS)

        return self.thickness

    def getDepth(self):
        if self.depth < self.MINDEPTH:
            self.violation = True

        if self.depth < 0:
            self.depth = random.uniform(self.MINDEPTH,2.0)

        return self.depth

    def getFitness(self):
        self.fitness = 0.01
        self.checkConstraint()

        # if any parameter violate, return 0.0 directly
        if self.violation:
            # reset the violation flag
            self.selfGenerating()
        else:
            self.fitness = 1/((1.10471*(math.pow(self.getLength(),2))*self.getDepth()) + (0.04811*self.getThickness()*self.getWidth()*(14.0+self.getDepth())))
            #geneString = "h: {} w: {} L:{} d:{} Fitness: {}".format(self.width,self.length,self.depth,self.thickness,1/fitness)
            #print (geneString)
            #os.system("echo {} >> testing.txt".format(geneString))
        
        return self.fitness

    def checkConstraint(self):
        self.violation = False
        h=self.getWidth()
        w=self.getLength()
        L=self.getDepth()
        d=self.getThickness()
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
        #px = 0.61423*(math.pow(10,6))*((d*math.pow(h,3))/6)*(1-(math.pow(30/48,1/d)/28))
        # print (h, d)
        px = 0.61423*(math.pow(10,6))*((d*math.pow(h,3))/6)*(1- (math.pow(math.exp(1), math.log(30/48)/d)))

        if (w - h) > 0 :
            self.violation=True
        elif (sx - 0.25) > 0:
            self.violation=True
        elif (tx - 13600) > 0:
            self.violation=True
        elif (ax - 30000) > 0:
            self.violation = True
        elif ((0.10471*math.pow(w,2)) + (0.04811*h*d*(14+L)) - 5) > 0:
            self.violation = True
        elif (0.125 - w) > 0:
            self.violation = True
        elif (6000 - px) > 0:
            self.violation = True

    def selfGenerating(self):
        self.width = random.uniform(0.1, self.MAXWIDTH)
        self.length = random.uniform(self.MINLENGTH,self.width)
        self.depth = random.uniform(self.MINDEPTH,2.0)
        self.thickness = random.uniform(6,self.MAXTHICKNESS)
        self.ind = [self.width, self.length, self.depth, self.thickness]
        return

def simpleArithmeticCrossover(parent1,parent2):
    child1 = Individual()
    child2 = Individual()

    genePosition=random.randint(0,child1.getGeneSize()-1) # take in size of gene from variable
    for x in range(child1.getGeneSize()):
        if x >= genePosition:
            geneValue1 = (recombinationVar*parent2.getIndividualGene(x)+(1-recombinationVar)*parent1.getIndividualGene(x))
            geneValue2 = (recombinationVar*parent1.getIndividualGene(x)+(1-recombinationVar)*parent2.getIndividualGene(x))
            #geneValue2 = parent1.getIndividualGene(x)
            #geneValue1 = parent2.getIndividualGene(x)
            child1.setParticularGene(x,geneValue1)
            child2.setParticularGene(x,geneValue2)
        else:
            child1.setParticularGene(x,parent1.getIndividualGene(x))
            child2.setParticularGene(x,parent2.getIndividualGene(x))

    # return both children
    return child1,child2

def Mutation(parent,iteration):
    # Init child1 as parent to undergo mutation
    child = parent
    ProbOfMutation = random.random()
    
    #c = random.uniform(0.8,1.0)

    # init mu and sigma
    mu,sigma = 0,0.1

    if iteration < 1500*0.2:
        mu, sigma = 0, 1
    elif iteration > 1500*0.2:
        mu, sigma = 0, 0.1

    #s = np.random.normal(mu, sigma, 1000)
    #guassian_formulat = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (s - mu)**2 / (2 * sigma**2))
    #print ("gaussian: {}".format(guassian_formulat))
    #deltasigma = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2)
    #num = min(10, max(0, random.gauss(0, 2)))
    # print (child.getIndividualGeneArray())
    for _ in range(child.getGeneSize()):
        if (ProbOfMutation > 0.05):
            num = random.gauss(mu,sigma)
            #num = np.random.normal(mu,sigma)
            RandomgeneValue = child.getIndividualGene(_) + num
            # print ("MR: {} Gene @ {}: to geneVal: {}".format(MutationRate,_,RandomgeneValue))
            child.setParticularGene(_, RandomgeneValue)

    # print (child.getIndividualGeneArray())
    # return mutated child
    return child

# FPS selection
# return the parent based on its fitness proportional selection
def FPS(pop):
    max = sum(c.getFitness() for c in pop)
    pick = random.uniform(0, max)
    current = 0.0
    for c in pop:
        current += c.fitness
        if current > pick:
            return c

def main():
    popSize = 100
    pop = Population(popSize,1)
    for y in range(1500):
        newPop = Population(popSize,0)
        newPop.insertPopulation(pop.getFittest())
        #os.system("echo Iteration: {} Fitness: {}>> testing.txt".format(y, 1/(pop.getFittest().getFitness())))
        print ("Iteration: {} Fitness: {}".format(y, 1/(pop.getFittest().getFitness())))
        for x in range(int(popSize/2)):
            #parent1 = pop.getParent()
            #parent2 = pop.getParent()
            parent1 = FPS(pop.getPopulation())
            parent2 = FPS(pop.getPopulation())
            #if (parent1.getIndividualGeneArray() == parent2.getIndividualGeneArray()):
                #geneString = "w: {} h: {} L:{} d:{}".format(w,h,L,d)
                #os.system("echo {} {} >> gene.txt".format(parent1.getIndividualGeneArray(),parent2.getIndividualGeneArray()))
            #print (parent1.getIndividualGeneArray())
            #print (parent2.getIndividualGeneArray())
            # check the fitness of the parent, if the fitness is not good, then don't select them.
            # set fitness proportional selection for the parent.
            #fitness1 = parent1.getFitness()
            #fitness2 = parent2.getFitness()

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


def validate_checkConstraint():
    fitness = 0.0

    L = 1.4313509130700104
    d = 7.25774482387524
    w = 0.5794571665426457
    h = 0.6109559551234784

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

# take in paramter of iteration and the current fitness level,
# - if the fitness level increase, control the mu to take the best fitness and slowly reduce it.
# in earlier stage, set the mu to sigma to be higher.
# slowly reduce the sigma in later stage.
def selfAdaptiveGaussianMutationRate():
    mu, sigma = 0, 0.1 # mean and standard deviation
    #s = np.random.normal(mu, sigma, 10)

    #print (abs(mu - np.mean(s)) < 0.01)
    #print (abs(sigma - np.std(s, ddof=1)) < 0.01)

    #num = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (s - mu)**2 / (2 * sigma**2))
    num = np.random.normal(mu,sigma)
    return num

#for _ in range(100):
#    print (selfAdaptiveGaussianMutationRate())
#    mu, sigma = 0,0.1
#    print (random.gauss(mu,sigma))
fuzzy_system(1,0.5)
#main()
#print (validate_checkConstraint())
