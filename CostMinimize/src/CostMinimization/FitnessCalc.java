package CostMinimization;
import java.util.ArrayList;

public class FitnessCalc {

    static byte[] solution = new byte[128];
    static ArrayList<Project> projects = new ArrayList<Project>();
    static int fitnessEvaluated = 0;

    /* Public methods */
    // Set a candidate solution as a byte array
    public static void setSolution(byte[] newSolution) {
        solution = newSolution;
    }
    
    public static void addProject(Project project){
        projects.add(project);
    }
    
    public static Project getProject(int index){
        return projects.get(index);
    }

    // To make it easier we can use this method to set our candidate solution 
    // with string of 0s and 1s
    static void setSolution(String newSolution) {
        solution = new byte[newSolution.length()];
        // Loop through each character of our string and save it in our byte 
        // array
        for (int i = 0; i < newSolution.length(); i++) {
            String character = newSolution.substring(i, i + 1);
            if (character.contains("0") || character.contains("1")) {
                solution[i] = Byte.parseByte(character);
            } else {
                solution[i] = 0;
            }
        }
    }

}