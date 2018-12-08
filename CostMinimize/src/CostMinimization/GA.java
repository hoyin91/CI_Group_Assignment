package CostMinimization;


public class GA {

    public static void main(String[] args) {
       // Show each rule (and degree of support)
       Helper.getMutationRate();
        //Set Problem
        Helper.problem = Problem.PRESSURE_VESSEL;
        // Create an initial population
        Population myPop = new Population(50, true);
        
        
        // Evolve our population until we reach an optimum solution
        int generationCount = 0;
        //Initial fitness
        //System.out.println("Generation: " + generationCount + " Fittest: " + Math.floor(myPop.getFittest().getFitness()*100)/100 + " Genes: " + myPop.getFittest());
        for (int i=0;i < 500; i++) {
            generationCount++;
            //myPop.getFittest().getFitness();
            myPop = Algorithm.evolvePopulation(myPop);
            System.out.println("Generation: " + generationCount + " Fittest: " + 1/myPop.getFittest().getFitness() + " Mean: " + myPop.getFitnessMean() +  " Genes: " + myPop.getFittest());
            
        }
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
                    mapping = "w";
                if (i == 2)
                    mapping = "d";
                if (i == 3)
                    mapping = "h";
                System.out.print(mapping + ":");
                System.out.print(myPop.getFittest().getGene(i));
                System.out.print(", ");
        }
        System.out.println("");

    }
}