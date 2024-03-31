import yaml
with open('menu/games.yml') as f:
    games = yaml.load(f, Loader=yaml.FullLoader)

with open('menu/admin.yml') as f:
    admin = yaml.load(f, Loader=yaml.FullLoader)

def get_game_by_id(game_id):
    for game in games:
        if game['id'] == game_id:
            return game
    
    for a in admin:
        if a['id'] == game_id:
            a.update({'path': '..'})
            return a

    return None

# import soundfile as sf
# import sounddevice as sd
