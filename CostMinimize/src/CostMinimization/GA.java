package CostMinimization;

public class GA {

    public static void main(String[] args) {

        //Set Problem
        Helper.problem = Problem.WELDED_BEAM;
        // Create an initial population
        Population myPop = new Population(1000, true);
        
        
        // Evolve our population until we reach an optimum solution
        int generationCount = 0;
        //Initial fitness
        System.out.println("Generation: " + generationCount + " Fittest: " + Math.floor(myPop.getFittest().getFitness()*100)/100 + " Genes: " + myPop.getFittest());
        for (int i=0;i < 1000; i++) {
            generationCount++;
            //myPop.getFittest().getFitness();
            myPop = Algorithm.evolvePopulation(myPop);
            System.out.println("Generation: " + generationCount + " Fittest: " + Math.floor(myPop.getFittest().getFitness()*10000)/10000 + " Genes: " + myPop.getFittest());
            
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
                    mapping = "d";
                if (i == 2)
                    mapping = "w";
                if (i == 3)
                    mapping = "h";
                System.out.print(mapping + ":");
                System.out.print(myPop.getFittest().getGene(i));
                System.out.print(", ");
        }
        System.out.println("");

    }
}