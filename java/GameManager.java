import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;

public class GameManager {

    GameLibrary gameLibraryClass = new GameLibrary();
    Scanner scanner = new Scanner(System.in);

    Boolean flag_run = true;
    ArrayList<Game> library = new ArrayList<>();

    public void start() {

        library = gameLibraryClass.loadData();

        // Print welcome message + ASCII art
        print("\n---------------Welcome to sTUIpid---------------");
        print("       _______________ ___.___       .__    .___\n" +
                        "  _____\\__    ___/    |   \\   |_____ |__| __| _/\n" + 
                        " /  ___/ |    |  |    |   /   \\____ \\|  |/ __ | \n" + 
                        " \\___ \\  |    |  |    |  /|   |  |_> >  / /_/ | \n" + 
                        "/____  > |____|  |______/ |___|   __/|__\\____ | \n" +
                        "     \\/                       |__|           \\/ ");
        printDivider(48);

        // Main loop
        while (flag_run) {
            print("Select an option:\n"+
                "1. View all games\n"+
                "2. View a specific game\n"+
                "3. Exit\n"
            );

            // Await input
            String input = scanner.nextLine();

            switch (input.toString()) {
                case "1" -> printLibrary();
                case "2" -> gameSelector();
                case "3" -> exit();
                default -> print("Invalid option, try again.");
            }
        }
    }

    public void print(String text) {
        System.out.println(text);
    }

    public void printDivider(Integer length) {
        System.out.println("\n" + "-".repeat(length) + "\n");
    }

    public void exit() {
        flag_run = false;
    }

    public void printLibrary() {
        printDivider(48);
        for (int i = 0; i < library.size(); i++) {
            Game current_game = library.get(i);
            String displayName = current_game.name;

            if (displayName.length() > 25) {
                String[] words = displayName.split(" ");
                Integer limit = Math.min(words.length, 4);
                words[limit - 1] = words[limit - 1].substring(0, 1) + "...";
                displayName = String.join(" ", Arrays.copyOfRange(words, 0, limit));
            }

            System.out.printf("%-30s %5.1f h%n", displayName, current_game.playtime / 60.0);
        }
        print("\n");
        printDivider(48);
    }

    public void gameSelector() {
        print("Enter the name of the game you want to choose:");
        String game_name = scanner.nextLine().toLowerCase();
        ArrayList<Game> optionList = new ArrayList<>();

        for (Game currGame : library) {

            // Filter out special characters + make lowercase
            String filtered_name = currGame.name
                .replaceAll("[^a-zA-Z0-9 ]", "")
                .toLowerCase(); 

            if (filtered_name.contains(game_name)) {
                optionList.add(currGame);
            }
        }

        Game selectedGame;

        if (optionList.size() == 1) {
            selectedGame = optionList.get(0);
            showGameStatsAndDetails(selectedGame);
        } else {
            print("Multiple games found, please select one:");

            for (Integer i = 0; i < optionList.size(); i++) {
                Game currGame = optionList.get(i);
                print(i+1 + ". " + currGame.name);
            }

            try {
                Integer selected_game_index = Integer.parseInt(scanner.nextLine());
                selectedGame = optionList.get(selected_game_index);
                showGameStatsAndDetails(selectedGame);
            } catch (NumberFormatException e) {
                print("Option is not a number, try again.");
                gameSelector();
            } catch (IndexOutOfBoundsException e) {
                print("Option is not on the list, try again.");
                gameSelector();
            } catch (Exception e) {
                print("An unexpected Error has occured: " + e);
            }
        }
    }

    public void showGameStatsAndDetails(Game game) {
        printDivider(65);

        System.out.printf("  %-30s %9s %16s%n", "Game", "Playtime", "Recent Playtime");
        System.out.printf("  %-30s %9s %16s%n", "----", "--------", "---------------");
        System.out.printf("  %-30s %8.1fh %15.1fh%n", game.name, game.playtime / 60.0, game.playtime_2weeks / 60.0);

        showASCIIart(game.appid);
        print(game.appid);
        printDivider(65);
    }

    public void showASCIIart(String appid) {
        try {
            Process p = new ProcessBuilder("python3", "asciiMaker.py", appid)
                .inheritIO()
                .directory(new File("../python"))
                .start();
            p.waitFor();   
        } catch (Exception e) {
            System.out.println("(ERR) An Error Occured While Generating ASCII image");
            System.err.println(e);
        }
    }
}
