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

    
    double w;
    double d;
    double L;
    public CompressionDesignIndividual(){
        setGeneLength(3);
    }
    
    @Override
    public void generateIndividual(){
        
        do{
            setGene(0, Helper.GenerateRandom(0.05, 2));
            setGene(1, Helper.GenerateRandom(0.25, 1.3));
            setGene(2, Helper.GenerateRandom(2, 15));
        } while (constraintsViolated());

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
        
        if (w < 0.05){
            setGene(0, 0.05);
        }
        if (w > 2){
            setGene(0, 2);
        }
        if (d < 0.25){
            setGene(1, 0.25);
        }
        if (d > 1.3){
            setGene(1, 1.3);
        }
        if (L < 2){
            setGene(2, 2);
        }
        if (L > 15){
            setGene(2, 15);
        }
        
        if (constraintsViolated())
            generateIndividual();
    }
    
    @Override
    public boolean constraintsViolated(){
        Refresh();
        double g1x = 1 - ((Math.pow(d,3)*L) / (71785*Math.pow(w,4)));
        double g2x = 1 - ((140.45*w)/(Math.pow(d, 2)*L));
        double g3x = ((w+d)/1.5) - 1;
        double g4x = ((d*((4*d)-w))/(Math.pow(w,3)*((12566*d)-w))) + (1/(5108*Math.pow(w, 2))) - 1;
        
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
        w = getGene(0);
        d = getGene(1);
        L = getGene(2);
    }

}
