package CostMinimization;

public abstract class Individual {

    private double[] genes;
    // Cache
    protected double fitness = -1;
    protected double[] stepSize;
    
    public final void setGeneLength(int length){
        genes = new double[length];
        stepSize = new double[length];
    }
    
    // Create a random individual
    public abstract void generateIndividual();
    public abstract double getFitness();
    public abstract boolean constraintsViolated();
    public abstract void CheckLimit();
    
    public double getGene(int index) {
        return genes[index];
    }

    public void setGene(int index, double value) {
        genes[index] = value;
        fitness = -1;
    }
    
    public void setStepSize(int index, double mutateStepSize){
        stepSize[index] = mutateStepSize;
    }
    
    public double getStepSize(int index){
        return stepSize[index];
    }

    /* Public methods */
    public int size() {
        return genes.length;
    }
    

    @Override
    public String toString() {
        String geneString = "";
        for (int i = 0; i < size(); i++) {
            geneString += getGene(i);
            geneString += ", ";
        }
        return geneString;
    }
}