/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package CostMinimization;

import java.nio.file.FileSystems;
import java.nio.file.Path;
import net.sourceforge.jFuzzyLogic.FIS;

/**
 *
 * @author Xiong
 */
public class Helper {
    public static Problem problem;
    public static double GenerateRandom(double min, double max){
        return (Math.random() * (max - min)) + min;
    }
    
    public static double root(double base, double n){
        return Math.pow(Math.E, Math.log(base)/n);
    }
    
    public static Individual GetIndividual(){
        Individual indiv;
        switch (problem){
            case WELDED_BEAM:
                indiv = new WeldedBeamIndividual();
                break;
            case PRESSURE_VESSEL:
                indiv = new PressureVesselDesignIndividual();
                break;
            case COMPRESSION_DESIGN:
                indiv = new CompressionDesignIndividual();
                break;
            default:
                indiv = null;
        }
        
        return indiv;
    }
    
    public static double calculateSD(double numArray[])
    {
        double sum = 0.0, standardDeviation = 0.0;
        int length = numArray.length;

        for(double num : numArray) {
            sum += num;
        }

        double mean = sum/length;

        for(double num: numArray) {
            standardDeviation += Math.pow(num - mean, 2);
        }

        return Math.sqrt(standardDeviation/length);
    }
    
    public static double getMutationRate(){
        System.out.println("Working Directory = " +
              System.getProperty("user.dir"));
        Path path = FileSystems.getDefault().getPath("test.fcl");
        FIS fis = FIS.load("C:\\Users\\yitxi\\Documents\\GitHub\\CI_Group_Assignment\\CostMinimize\\src\\CostMinimization\\test.fcl", true); // Load from 'FCL' file
        //FIS fis = FIS.load(path.toString(), true);
        fis.setVariable("service", 3); // Set inputs
        fis.setVariable("food", 7);
        fis.evaluate(); // Evaluate
        System.out.println("Output value:" + fis.getVariable("tip").getValue()); // Show output variable
        
        return 0;
    }
}
