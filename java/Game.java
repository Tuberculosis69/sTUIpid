import java.util.ArrayList;

public class Game {
    String name;
    String appid;
    Boolean recently_played;

    // Playtime is in minutes
    Integer playtime;
    Integer playtime_2weeks;

    // date:str, playtime:int
    ArrayList<Snapshot> snapshots = new ArrayList<>();

    public Integer getPlaytime() {
        Snapshot latestSnapshot = snapshots.get(snapshots.size() - 1); 
        return latestSnapshot.playtime;
    }
}

