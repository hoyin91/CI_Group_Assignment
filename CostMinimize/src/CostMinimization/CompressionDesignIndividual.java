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
public class CompressionDesignIndividual extends Individual {

    public CompressionDesignIndividual(){
        setGeneLength(3);
    }
    
    @Override
    public void generateIndividual(){
        
    }
    
    @Override
    public double getFitness(){
        return 0;
    } 
    
    @Override
    public void CheckLimit(){
        
    }
    
    @Override
    public boolean constraintsViolated(){
        return true;
    }

}
