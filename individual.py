import random
import numpy as np
import math

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
        self.depth = random.uniform(self.MINDEPTH,10.0)
        self.thickness = random.uniform(6,self.MAXTHICKNESS)
        self.ind = [self.width, self.length, self.depth, self.thickness]
        self.fitness = 0.0

        self.checkConstraint()
        while self.violation:
            self.selfGenerating()
            self.checkConstraint()
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
        self.fitness = 0.0001
        self.checkConstraint()

        # if any parameter violate, return 0.0 directly
        if self.violation:
            self.selfGenerating()
            # reset the violation flag
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
