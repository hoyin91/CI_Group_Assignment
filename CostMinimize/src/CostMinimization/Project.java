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
public class Project {
    private double _profit;
    private double _y1Expense;
    private double _y2Expense;
    private double _y3Expense;
    String _projectName;
    
    public Project(String projectName, double profit, double y1Expense, double y2Expense, double y3Expense){
        _profit = profit;
        _y1Expense = y1Expense;
        _y2Expense = y2Expense;
        _y3Expense = y3Expense;
        _projectName = projectName;
    }
    
    public double getProfit(){
        return _profit;
    }
    
    public double getY1Expense(){
        return _y1Expense;
    }
    
    public double getY2Expense(){
        return _y2Expense;
    }
    
    public double getY3Expense(){
        return _y3Expense;
    }
}
