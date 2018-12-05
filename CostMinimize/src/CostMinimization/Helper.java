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
    public static double GenerateRandom(double min, double max){
        return (Math.random() * ((max - min) + 1)) + min;
    }
    
    public static double root(double base, double n){
        return Math.pow(Math.E, Math.log(base)/n);
    }
}
