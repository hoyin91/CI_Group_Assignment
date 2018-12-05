package CostMinimization;

public class Algorithm {

    /* GA parameters */
    private static final double uniformRate = 0.5;
    private static final double mutationRate = 0.05;
    private static final int tournamentSize = 5;
    private static final boolean elitism = true;
   

    /* Public methods */
    
    // Evolve a population
    public static Population evolvePopulation(Population pop) {
        Population newPopulation = new Population(pop.size(), false);

        // Keep our best individual
        if (elitism) {
            newPopulation.saveIndividual(0, pop.getFittest());
        }

        // Crossover population
        int elitismOffset;
        if (elitism) {
            elitismOffset = 1;
        } else {
            elitismOffset = 0;
        }
        // Loop over the population size and create new individuals with
        // crossover
        for (int i = elitismOffset; i < pop.size(); i++) {
            Individual indiv1 = tournamentSelection(pop);
            Individual indiv2 = tournamentSelection(pop);
            //Individual indiv1 = fpSelection(pop);
            //Individual indiv2 = fpSelection(pop);
            Individual newIndiv = crossover(indiv1, indiv2);
            newIndiv.CheckLimit();
            
            newPopulation.saveIndividual(i, newIndiv);
        }

        // Mutate population
        for (int i = elitismOffset; i < newPopulation.size(); i++) {
            mutate(newPopulation.getIndividual(i));
            newPopulation.getIndividual(i).CheckLimit();
        }

        return newPopulation;
    }

    // Crossover individuals
    private static Individual crossover(Individual indiv1, Individual indiv2) {
        Individual newSol = new WeldedBeamIndividual();
        
        double a = Math.random();
        double b = 1 - Math.random();
        // Loop through genes
        for (int i = 0; i < indiv1.size(); i++) {
            // Crossover
            newSol.setGene(i, (a*indiv1.getGene(i))+(b*indiv2.getGene(i)));
        }
        return newSol;
    }
    //1-point crossover
    private static Individual crossover2(Individual indiv1, Individual indiv2){
        Individual newSol = new WeldedBeamIndividual();
        
        int point = (int) ((Math.random()*0.7 + 0.2) * (newSol.size() - 1));
        
        //Get gene from indiv1
        for (int i = 0; i < point; i++){
            newSol.setGene(i, indiv1.getGene(i));
        }
        //Get gene from indiv2
        for (int i = point; i < newSol.size(); i ++ ){
            newSol.setGene(i, indiv2.getGene(i));
        }
       
        return newSol;
    }

    // Mutate an individual
    private static void mutate(Individual indiv) {
        // Loop through genes
        for (int i = 0; i < indiv.size(); i++) {
            if (Math.random() <= mutationRate) {
                // Create random gene
                double random = Helper.GenerateRandom(0, 2)*indiv.getGene(i);
                indiv.setGene(i, random);
            }
        }
    }

    // Select individuals for crossover
    private static Individual tournamentSelection(Population pop) {
        // Create a tournament population
        Population tournament = new Population(tournamentSize, false);
        // For each place in the tournament get a random individual
        for (int i = 0; i < tournamentSize; i++) {
            int randomId = (int) (Math.random() * pop.size());
            tournament.saveIndividual(i, pop.getIndividual(randomId));
        }
        // Get the fittest
        Individual fittest = tournament.getFittest();
        return fittest;
    }
    
    //Select individual for crossover using fps
    private static Individual fpSelection(Population pop){
        int fitnessSum = 0;
        for (int i = 0; i < pop.size(); i++){
            Individual individual = pop.getIndividual(i);
            fitnessSum += individual.getFitness();
        }
        double randomValue = Math.random() * fitnessSum;
        int selectedInd = 0;
        int partialSum = 0;
        for (int i= 0; i < pop.size() ; i++) {
             partialSum += pop.getIndividual(i).getFitness();
             if (partialSum > randomValue){
                 selectedInd = i;
                 break;
             }
        }
        //System.out.println("Crossover indiv index: " + selectedInd);
        return pop.getIndividual(selectedInd);
    }
}