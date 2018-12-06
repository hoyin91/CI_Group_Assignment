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

    double L;
    double w;
    double d;
    public CompressionDesignIndividual(){
        setGeneLength(3);
    }
    
    @Override
    public void generateIndividual(){
        setGene(0, Helper.GenerateRandom(2, 15));
        setGene(1, Helper.GenerateRandom(0.05, 2));
        setGene(2, Helper.GenerateRandom(0.25, 1.3));
        
        CheckLimit();
    }
    
    @Override
    public double getFitness(){
        Refresh();
        double fx = (L + 2)*Math.pow(w,2)*d;
        
        return 1/fx;
    } 
    
    @Override
    public void CheckLimit(){
        Refresh();
        
        if (L < 2 || L > 15){
            setGene(0, Helper.GenerateRandom(2, 15));
        }
        if (w < 0.05 || w > 2){
            setGene(1, Helper.GenerateRandom(0.05, 2));
        }
        if (d < 0.25 || d > 1.3){
            setGene(2, Helper.GenerateRandom(0.25, 0.85));
        }
        
        if (constraintsViolated())
            generateIndividual();
    }
    
    @Override
    public boolean constraintsViolated(){
        Refresh();
        double g1x = 1 - ((Math.pow(d,3)*L) / (7178*Math.pow(w,4)));
        double g2x = 1 - ((140.45*w)/(Math.pow(d, 2)*L));
        double g3x = ((2*(w+d))/3) - 1;
        double g4x = ((d*((4*d)-w))/(Math.pow(w,4)*(12566*d-w))) + (1/(5108*Math.pow(w, 2))) - 1;
        
        if (g1x > 0)
            return true;
        if (g2x > 0)
            return true;
        if (g3x > 0)
            return true;
        if (g4x > 0)
            return true;
        
        
        return false;
    }
    
    private void Refresh(){
        L = getGene(0);
        w = getGene(1);
        d = getGene(2);
    }

}
