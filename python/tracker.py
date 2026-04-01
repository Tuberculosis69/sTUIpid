# This file is redundant but I'll keep it in case I restructure the code one day
from GameManager import GameManager

def start():
    manager = GameManager()
    manager.sort_by_playtime()
    manager.save_snapshot()
    
