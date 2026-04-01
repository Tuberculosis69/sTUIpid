import api as api
from operator import itemgetter
import json
from datetime import date

# TODO !! REFACTOR SHIT CODE !!

class GameManager:
    
    def __init__(self):
        
        self.games = api.get_owned_games()
        self.recent_games = api.get_recent_games()
        self.player_data = api.get_player_summary()
        
        # Blacklisted games i want to exclude from the data
        with open(r"blacklist_spreadsheet.txt", 'r', encoding='utf-8') as f:
            blacklist = [line.strip() for line in f.readlines()]
            
        # Remove blacklisted items
        self.sorted_data = []
        for game in self.games:
            curr_name = game["name"]
            if curr_name in blacklist:
                print(f"(LOG) Excluded Game: {curr_name}")
            else:
                self.sorted_data.append({
                    "appid"    : game["appid"], 
                    "name"     : game["name"],
                    "playtime_mins" : game["playtime_forever"],
                    "img_icon_url"      : game["img_icon_url"]
                })
                print(f"(LOG) Included Game: {curr_name}")

    def sort_by_playtime(self):
        self.sorted_data = sorted(self.sorted_data, key=itemgetter('playtime_mins'), reverse=True)
        
    def save_snapshot(self):
        
        snapshot_date = str(date.today())
        data = {}
        
        try: 
            with open("../data.json", "r") as f:
                data = json.load(f)
                
        except Exception as e:
            print(f"(ERR) Error loading .json : {e}")
            
        games = self.sorted_data
        recent_games = self.recent_games
        for game in games:
            appid = game["appid"]
            name = game["name"]
            playtime_mins = game["playtime_mins"]
            img_icon_url = game["img_icon_url"]
            
            # Assume not a recent game
            playtime_2weeks_mins = 0
            recently_played = False
            
            # Check if game exists, if so add a snapshot, else make a new game entry
            if str(appid) in data.keys():
                
                # Check for duplicate entries before adding
                no_duplicate_date = True
                snapshots = data[str(appid)]["snapshots"]
                for snapshot in snapshots:
                    if snapshot["date"] == snapshot_date:
                        no_duplicate_date = False
                if no_duplicate_date:
                    data[str(appid)]["snapshots"].append({
                        "date" : snapshot_date, "playtime_mins" : playtime_mins
                    })
                
            else:
                data[appid] = {
                    "name" : name,
                    "recently_played" : recently_played,
                    "playtime_2weeks" : playtime_2weeks_mins,
                    "snapshots" : [{
                            "date" : snapshot_date, "playtime_mins" : playtime_mins
                        }],
                    "img_icon_url" : img_icon_url
                }
                print(f"(LOG) Added new game: {name}")
                print(f"(LOG) Saving {name} icon image...")
                api.save_img(appid, img_icon_url)
                
        # data.json might be empty which will cause errors for the next for loop
        # to prevent this, save premptively in case the file is empty
        with open("../data.json", "w") as f:
            json.dump(data, f, indent=4)
            
        try: 
            with open("../data.json", "r") as f:
                data = json.load(f)
                
        except Exception as e:
            print(f"(ERR) Error loading .json : {e}")
                            
        # Loop through all recent games and update accordingly    
        for game in recent_games:
            appid = str(game["appid"])
            playtime_2weeks_mins = game["playtime_2weeks"]
            
            try:
                data[appid]["recently_played"] = True
                data[appid]["playtime_2weeks"] = playtime_2weeks_mins
            except KeyError as e: 
                # There was a game that only showed up in the get_recent_games call but not the get_owned_games call,
                # despite the include_played_free_games flag, so this is a fallback for this edge case that adds it to the data anyways
                data[appid] = {
                    "name" : game["name"],
                    "recently_played" : True,
                    "playtime_2weeks" : recent_games[i]["playtime_2weeks"],
                    "snapshots" : [{
                            "date" : snapshot_date, "playtime_mins" : game["playtime_forever"]
                        }],
                    "img_icon_url" : recent_games[i]["img_icon_url"]
                }
                print(f"(WAR) A game with appid {e} is only appearing in get_recent_games but not get_owned_games.")
                
            
    
        with open("../data.json", "w") as f:
            json.dump(data, f, indent=4)
            
        print("\nFinished Updating Data\n")
    
    # Just in case, this can save all images at once
    def save_images(self):
        data = self.sorted_data
        
        for game in data:
            appid = game["appid"]
            img_icon_url = game["img_icon_url"]
            api.save_img(appid, img_icon_url)