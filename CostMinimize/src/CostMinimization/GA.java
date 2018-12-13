package CostMinimization;


public class GA {

    public static void main(String[] args) {
       // Show each rule (and degree of support)
        //Set Problem
        Helper.problem = Problem.WELDED_BEAM;
        // Create an initial population
        Population myPop = new Population(50, true);
        double fitnessMean = 0;
        
        
        // Evolve our population until we reach an optimum solution
        int generationCount = 0;
        //Initial fitness
        //System.out.println("Generation: " + generationCount + " Fittest: " + Math.floor(myPop.getFittest().getFitness()*100)/100 + " Genes: " + myPop.getFittest());
        for (int k = 0; k < 1; k++){
            myPop = new Population(50, true);
            for (int i=0;i < 500; i++) {
                generationCount = i;
                //myPop.getFittest().getFitness();
                myPop = Algorithm.evolvePopulation(myPop);
                System.out.println("Generation: " + generationCount + " Fittest: " + 1/myPop.getFittest().getFitness() + " Mean: " + 1/myPop.getFitnessMean() +  " Genes: " + myPop.getFittest());
            }
            Algorithm.genNoImprovement = 0;
            Algorithm.genWithImprovement = 0;
            fitnessMean += myPop.getFittest().getFitness();
        }
        fitnessMean = 1 / (fitnessMean/100);
        
        System.out.println("FitnessMean: " + fitnessMean);
        
        
        
        String mapping = "";
        //System.out.println("Generation: " + generationCount + " Fittest: " + myPop.getFittest().getFitness());
        System.out.println("Solution found!");
        System.out.println("Generation: " + generationCount);
        System.out.println("Genes:");
        System.out.println(myPop.getFittest());
        System.out.println("Selected project:");
        for (int i=0; i < myPop.getFittest().size(); i++){
                if (i == 0)
                    mapping = "L";
                if (i == 1)
                    mapping = "d";
                if (i == 2)
                    mapping = "w";
                if (i == 3)
                    mapping = "h";
                System.out.print(mapping + ":");
                System.out.print(myPop.getFittest().getGene(i));
                System.out.print(", \n");
        }
        System.out.println(Helper.generatedIndiv);

    }
}