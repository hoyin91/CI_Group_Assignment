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
public class WeldedBeamIndividual extends Individual {
    
    public double L;
    public double d;
    public double w;
    public double h;
    
    public WeldedBeamIndividual(){
        setGeneLength(4);
    }
    
    @Override
    public void generateIndividual(){
        do{
            setGene(0, Helper.GenerateRandom(0.1, 5));
            setGene(1, Helper.GenerateRandom(0, 10));
            setGene(2, Helper.GenerateRandom(0.1, 2));
            setGene(3, Helper.GenerateRandom(0, 2));
        }while(constraintsViolated());
    }
    
    @Override
    public double getFitness(){
        Refresh();
        
        if (fitness == -1){
            double fx = (1.10471 * Math.pow(w, 2) * L) + (0.04811 * d * h)*(14.0 + L);
            fitness = 1/fx;
        }
        return fitness;
    }
    
    @Override
    public void CheckLimit(){
        
            Refresh();
            if (L <= 0.1)
                setGene(0, Helper.GenerateRandom(0.1, 5));
            if (d > 10)
                setGene(1, Helper.GenerateRandom(0.01, 9));
            if (w < 0.1)
                setGene(2, Helper.GenerateRandom(0.1, 2));
            if (h > 2)
                setGene(2, Helper.GenerateRandom(0.01, 2));
        
        if (constraintsViolated()){
            generateIndividual();
        }
    }
    
    @Override
    public boolean constraintsViolated(){
        
        Refresh();
        
        double ox = 504000 / (h*Math.pow(d, 2));
        double alpha = 6000 / (Math.sqrt(2)*w*L);
        double Q = 6000*(14 + L/2);
        double J = Math.sqrt(2)*w*L*((Math.pow(L,2)/6) + (Math.pow(w+d, 2)/2));
        double D = 0.5*Math.sqrt(Math.pow(L,2) + Math.pow(w+d, 2));
        double P = 0.61423 * Math.pow(10,6)*(d*Math.pow(h,3)/6)*(1-(Helper.root(30/48, d)/28));
        double Sx = 65856 / (30000*h*Math.pow(d,3));
        double beta = Q*D/J;
        double tx = Math.sqrt(Math.pow(alpha, 2) + (alpha*beta*L / D) + Math.pow(beta, 2));
        
        if ((w - h) > 0){
            return true;
            
        }
        if ((Sx - 0.25) > 0){
            return true;
        }
            
        if ((tx - 13600) > 0){
            return true;
        }
            
        if ((ox - 30000) > 0){
            return true;
        }
            
        if (((0.10471*Math.pow(w,2)) + (0.04811*h*d*(14+L)-5)) > 0){
            return true;
        }
            
        if ((0.125 - w) > 0){
            return true;
        }
            
        if ((6000 - P) > 0){
            return true;
        }
            
        
        return false;
    }
    
    private void Refresh()
    {
        L = getGene(0);
        d = getGene(1);
        w = getGene(2);
        h = getGene(3);
    }
            
    
}
