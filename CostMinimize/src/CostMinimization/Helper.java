/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package CostMinimization;

/**
 *
 * @author Xiong
 */
public class Helper {
    public static Problem problem;
    public static double GenerateRandom(double min, double max){
        return (Math.random() * ((max - min) + 1)) + min;
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
}