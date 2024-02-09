import yaml
with open('menu/games.yml') as f:
    games = yaml.load(f, Loader=yaml.FullLoader)

def get_game_by_id(game_id):
    for game in games:
        if game['id'] == game_id:
            return game
    return None

# import soundfile as sf
# import sounddevice as sd
