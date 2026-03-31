import java.io.File;

public class Main {
    public static void main(String[] args) {

        try {
            System.out.println("Updating Data...");
            Process p = new ProcessBuilder("python3", "main.py")
                .inheritIO()
                .directory(new File("../python"))
                .start();
            p.waitFor();   
        } catch (Exception e) {
            System.out.println("(ERR) An Error Occured While Loading the Data :(");
            System.err.println(e);
        }

        GameManager manager = new GameManager();
        manager.start();
    }
}
