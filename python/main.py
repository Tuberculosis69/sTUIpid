from GameManager import GameManager

manager = GameManager()
manager.sort_by_playtime()
manager.save_snapshot()
manager.save_profile_data()
print("\n   Finished Updating Data  \n")