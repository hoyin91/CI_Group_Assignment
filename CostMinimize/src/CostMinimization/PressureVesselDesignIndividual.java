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
public class PressureVesselDesignIndividual extends Individual {

    double Ts;
    double Th;
    double R;
    double L;
    public PressureVesselDesignIndividual(){
        setGeneLength(4);
    }
    
    @Override
    public void generateIndividual(){
        
        do {
            setGene(0, Helper.GenerateRandom(0.0625, 1));
            setGene(1, Helper.GenerateRandom(0.01, 6));
            setGene(2, Helper.GenerateRandom(10, 100));
            setGene(3, Helper.GenerateRandom(0, 200));
        } while(constraintsViolated());
        //CheckLimit();
    }
    
    @Override
    public double getFitness(){
        Refresh();
        double fx = (0.6224*Ts*R*L) + (1.7781*Th*Math.pow(R, 2)) + (3.1661*Math.pow(Ts, 2)*L) + (19.84*Math.pow(Th, 2)*R);
        return 1/fx;
    } 
    
    @Override
    public void CheckLimit(){
        Refresh();
        
        if (Ts < 0.0625)
            setGene(0, 0.0625);
        if (Th > (99*0.0625))
            setGene(1, (99*0.0625));
        if (R < 10)
            setGene(2, 10);
        if (L > 200)
            setGene(3, 200);
        
        if (constraintsViolated())
            generateIndividual();
    }
    
    @Override
    public boolean constraintsViolated(){
        Refresh();
        
        double g1x = (0.0193*R) - Ts;
        double g2x = (0.0095*R) - Th;
        double g3x = 1296000 - (Math.PI*Math.pow(R, 2)*L) - (4/3*Math.PI*Math.pow(R, 3));
        double g4x = L - 240;
        
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
        Ts = getGene(0);
        Th = getGene(1);
        R = getGene(2);
        L = getGene(3);
    }

}
