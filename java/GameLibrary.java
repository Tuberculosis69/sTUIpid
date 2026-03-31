import java.io.FileReader;
import java.util.ArrayList;
import java.io.FileNotFoundException;
import com.google.gson.*;

public class GameLibrary {

    public ArrayList<Game> loadData() {

        ArrayList<Game> library = new ArrayList<>(); 
        JsonObject data;

        try {
            data = JsonParser.parseReader(new FileReader("../data.json")).getAsJsonObject();    
        } catch (FileNotFoundException e) {
            data = new JsonObject();
            System.out.println("data.json not found!: " + e.getMessage());
        }

        // Iterate over all games
        for (String appId : data.keySet()) {
            JsonObject game_data = data.getAsJsonObject(appId);
            Game game = new Game();

            // Make the Game class
            String appid_str = appId;
            game.appid = appid_str;

            String name = game_data.get("name").getAsString();
            game.name = name;

            Boolean recently_played = game_data.get("recently_played").getAsBoolean();
            game.recently_played = recently_played;

            Integer playtime_2weeks = game_data.get("playtime_2weeks").getAsInt();
            game.playtime_2weeks = playtime_2weeks;

            JsonArray snapshots = game_data.get("snapshots").getAsJsonArray();
            for (Integer i = 0; i < snapshots.size(); i++) {
                JsonObject snapshot = snapshots.get(i).getAsJsonObject();
                String date = snapshot.get("date").getAsString();
                Integer playtime = snapshot.get("playtime_mins").getAsInt();

                game.snapshots.add(new Snapshot(date, playtime));
            }

            game.playtime = game.getPlaytime();
            library.add(game);
        }

        return library;
    }
}
