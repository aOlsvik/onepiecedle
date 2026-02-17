from game_data import GameData
from utils import load_json


def setup_game():
    onepiece_data = load_json('onepiece_data.json')
    character_data = onepiece_data['characters']
    character_data = [{key.lower().replace(" ", "_"): value for key, value in character.items()} for character in character_data]
    category_data = onepiece_data['categories']
    category_data = {key.lower().replace(" ", "_"): value for key, value in category_data.items()}
    game_data_options = {key.lower().replace(" ", "_") + "_options": list(value.get("options", [])) for key, value in category_data.items()}
    game_data = GameData(**game_data_options)
    return game_data, character_data